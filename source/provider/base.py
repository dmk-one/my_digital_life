from typing import (
    Dict, Callable, Union, Optional, Mapping, Iterable, Any, Type, Tuple, List, Sequence
)
import orjson as json
from sqlalchemy import (
    Table, Column, and_, any_, select, insert, update, delete, func, nullslast
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Insert, Update, Delete, distinct
from sqlalchemy.sql.expression import BinaryExpression, or_
from sqlalchemy.sql.selectable import Alias
from sqlalchemy_utils.functions import get_primary_keys

from source.service import domain
from source.session import async_session
from .shared.utils import clear_from_ellipsis
from . import models as orm_models


class AlchemyFilters:
    """
    Class that works with SQL clause building:
    {
        'name__like': '%some_name%',
        'id__in': [1, 2, 3]
    }
    Binds sql where clause to sql statement

    LOOKUP_STRING: str that separate fields and lookups:
    lookup = 'name' + '__' + 'ilike'.

    OPERATORS: this is available operators to use sql where clause:
    example: 'e' -> '==', 'l' -> '<', ...

    LOOKUP_OPERATORS: This is mapping of operators as keys ('e', 'le', 'ilike')
    and callable objects as keys. Every value i.e. every callable object is
    accepts orm model column (sqlalchemy.orm.InstrumentedAttribute) as first
    parameter and value (int, str, float, bool, Iterable[int, str, float], any)
    as second parameter and returns sqlalchemy.sql.expression.BinaryExpression.

    _mapper is required field, this is sqlalchemy orm model.

    _table is optional field, which will be pull out from _mapper field

    _joined_aliases is optional field, if you want to use and filter by aliases
    you have to define this field
    """

    LOOKUP_STRING = '__'
    EQUAL_OPERATOR = 'e'
    NOT_EQUAL_OPERATOR = 'ne'
    LESS_THAN_OPERATOR = 'l'
    LESS_THAN_OR_EQUAL_TO_OPERATOR = 'le'
    GREATER_THAN_OPERATOR = 'g'
    GREATER_THAN_OR_EQUAL_TO_OPERATOR = 'ge'
    LIKE_OPERATOR = 'like'
    ILIKE_IN_OPERATOR = 'ilike_in'
    ILIKE_OPERATOR = 'ilike'
    IN_OPERATOR = 'in'
    NOT_IN_OPERATOR = 'not_in'
    ALL_OBJECTS_FILTER = domain.ALL

    LOOKUP_OPERATORS = {
        EQUAL_OPERATOR: lambda c, v: c == v,
        NOT_EQUAL_OPERATOR: lambda c, v: c != v,
        LESS_THAN_OPERATOR: lambda c, v: c < v,
        LESS_THAN_OR_EQUAL_TO_OPERATOR: lambda c, v: c <= v,
        GREATER_THAN_OPERATOR: lambda c, v: c > v,
        GREATER_THAN_OR_EQUAL_TO_OPERATOR: lambda c, v: c >= v,
        LIKE_OPERATOR: lambda c, v: c.like(v),
        ILIKE_OPERATOR: lambda c, v: c.ilike(v),
        IN_OPERATOR: lambda c, v: c.in_(v),
        NOT_IN_OPERATOR: lambda c, v: c.not_in(v),
        ILIKE_IN_OPERATOR: lambda c, v: c.ilike(any_(v)),
    }

    _mapper: Type[orm_models.ORMBaseModel]
    _table: Table
    _joined_aliases: Tuple[Alias] = tuple()

    @property
    def _get_joined_aliases(self) -> Tuple[Optional[Alias]]:
        """
        Property that uses in another methods of this class. Returns
        self._joined_aliases if this field is defined
        """
        try:
            return self._joined_aliases
        except AttributeError:
            return tuple()

    @property
    def _get_mapper(self) -> Type[orm_models.ORMBaseModel]:
        """
        Property that uses in another methods to get orm model to work with
        """
        try:
            return self._mapper
        except AttributeError:
            raise Exception('Attribute Must Be Set Exception')

    def _get_table(
        self,
        reference_name: Optional[str] = None
    ) -> Union[Table, Alias]:
        """
        If reference_name passed as str tries to find reference in
        self._get_joined_aliases and if reference was found returns it,
        else tries to find reference in attributes of self._get_mapper,
        if reference not found so raises exception.
        Example:
        class OrmModel1(BaseOrmModel):
            __tablename__ = 'orm_model1'

            name = Column(String(255), nullable=False, unique=True)

        class OrmModel2(BaseOrmModel):
            __tablename__ = 'orm_model2'

            orm_model1_id = Column(BigInteger, ForeignKey('orm_model1.id'))
            orm_model1 = relationship('OrmModel1)

        and here to get OrmModel1 from OrmModel2 you have to use
        reference_name as relationship name -> 'orm_model1'

        or if there is joined_aliases like:
        _joined_aliases = [alias(2, name='aliased_orm_model1')]

        and here reference_name must be as alias name -> 'aliased_orm_model1'
        """
        if type(reference_name) is str:
            aliases: Tuple[Optional[Alias]] = self._get_joined_aliases
            filtered_aliases: Tuple[Optional[Alias]] = tuple(filter(
                lambda alias: reference_name in alias.name, aliases
            ))
            if filtered_aliases:
                return filtered_aliases[0]

            try:
                reference = getattr(self._get_mapper, reference_name)
                tables: List[Table] = reference.property.mapper.tables
                return tables[0]
            except (IndexError, AttributeError):
                raise Exception('Incorrect Reference Name Exception')

        try:
            return self._table
        except AttributeError:
            raise Exception('Attribute Must Be Set Exception')

    def _get_column(
        self,
        name: str,
        reference_name: Optional[str] = None,
    ) -> Column:
        """
        Tries to get column field from current table i.e. self._table by
        column name.

        If reference_name passed so first tries to get table or alias
        with reference_name and tries to get column from it by name
        """
        table: Union[Table, Alias] = self._get_table(reference_name=reference_name)

        column = table.columns.get(name)
        if isinstance(column, Column):
            return column

        raise Exception('Column Does Not Exist Exception')

    def _build_expression(
        self,
        lookup: str,
        value: Any,
        reference_name: Optional[str] = None,
    ) -> BinaryExpression:
        """
        Build sqlalchemy expression by passed lookup, value
        if value was passed as dict so this function will work recursively.
        Example:
        class OrmModel1(BaseOrmModel):
            __tablename__ = 'orm_model1'

            id = Column(BigInteger, primary_key=True)
            name = Column(String(255))

        class OrmModel2(BaseOrmModel):
            __tablename__ = 'orm_model2'

            id = Column(BigInteger, primary_key=True)
            name = Column(String(255))
            description = Column(String)

            orm_model1_id = Column(BigInteger, ForeignKey('orm_model1.id'))
            orm_model1 = relationship('OrmModel1')


        If _mapper or table has column with name that contained in lookup,
        this column will be used as column to build clause.
        So if _mapper is OrmModel2
        available lookups is id, name, description with operators like:
        'name__ilike', 'id__in', ...
        By default operator is EQUAL_OPERATOR

        reference_name is name of relationship field or alias to build
        expression by column of related table or alias.
        reference_name = 'orm_model1' means use column from OrmModel1 table.
        """
        if self.LOOKUP_STRING not in lookup:
            lookup = lookup + self.LOOKUP_STRING + self.EQUAL_OPERATOR

        column_name, *_, operator_name = lookup.split(self.LOOKUP_STRING)
        try:
            # self_method this is method that implemented in class Filters in Provider
            self_method: Callable = getattr(self, column_name)
            return self_method(operator_name, value)
        except AttributeError:
            pass

        column = self._get_column(name=column_name, reference_name=reference_name)

        # Handle if value passed as self.ALL_OBJECTS_FILTER
        # it forms expression like field != None
        # TODO wrong logic
        if value == self.ALL_OBJECTS_FILTER:
            operator_name = self.NOT_EQUAL_OPERATOR
            value = None

        lookup_operator = self.LOOKUP_OPERATORS.get(operator_name)
        if not callable(lookup_operator):
            raise Exception('Lookup Operator Not Found Exception')
        return lookup_operator(column, value)

    def build_where_clause(
        self,
        reference_name: Optional[str] = None,
        filters: Dict[str, Any] = {}
    ):
        """
        Builds where clause by passed lookups and values in filters.
        In for loop l is lookup and v is value. It works recursively
        if filters has dict value.
        #TODO Refactor it
        """
        E = []
        for l, v in filters.items():
            self_method = getattr(self, l, None)
            if self_method is not None:
                e = self_method(v)
            elif isinstance(v, Mapping):
                e = self.build_where_clause(reference_name=l, filters=v)
            else:
                e = self._build_expression(lookup=l, value=v, reference_name=reference_name)
            E.append(e)
        return and_(*E)


class BaseAlchemyModelProvider:
    """
    Base provider which implements query building by passing
    filters to it methods

    _mapper is required orm model class
    _usage_mappers is optional iterable object of orm model classes
    _table is optional object of sqlalchemy.Table, by default it pulls from
    _mapper
    _usage_aliases is optional iterable object of sqlalchemy Alias objects. It
    uses to build query with unknown to mapper fields

    _select_stmt is optional base select query with joins. It is used as base
    statement in where clause building. Default is sqlalchemy.select(_mapper)
    _select_count_stmt is optional base select count query with joins. It is
    used as base statement in where clause building. Default is
    sqlalchemy.select(sqlalchemy.func(sqlalchemy.count()).select_from(
        sqlalchemy.select(_mapper)
    )
    _insert_stmt is optional insert query. Default is sqlalchemy.insert(_mapper)
    _update_stmt is optional update query. Default is sqlalchemy.update(_mapper)
    _delete_stmt is optional delete query. Default is sqlalchemy.delete(_mapper)

    _first_pk_column_name is optional str which is name of _mapper first
    primary key column name. Default is 'id' and it gets from _mapper dynamically

    _sorting_columns is required iterable object of str. It contains names of
    _mapper columns to make order by them.

    _single_record_adapter is required async callable object to adapt
    from orm model instances to another type object. Uses in getting one object
    from db, in get method, in insert method, in update method and in
    get_or_insert method
    _multiple_records_adapter is required async callable object to adapt
    multiple orm models objects to another type object. It uses in select,
    bulk_insert, bulk_update methods

    """

    session: AsyncSession

    _mapper: Type[orm_models.ORMBaseModel]
    _usage_mappers: Optional[Tuple[Type[orm_models.ORMBaseModel]]] = None

    _table: Optional[Table] = None
    _usage_aliases: Optional[Tuple[Alias]] = tuple()

    _select_stmt: Optional[Select] = None
    _select_count_stmt: Optional[Select] = None
    _insert_stmt: Optional[Insert] = None
    _update_stmt: Optional[Update] = None
    _delete_stmt: Optional[Delete] = None

    _first_pk_column_name: Optional[str] = None

    _sorting_columns: Tuple[str]

    _single_record_adapter: Callable
    _multiple_records_adapter: Callable

    _does_not_exist_exception: Optional[str] = 'Object Does Not Exist'


    class Filters(AlchemyFilters):
        """
        Class that implements query clause binding behavior
        """

    @property
    def _get_mapper(self) -> Type[orm_models.ORMBaseModel]:
        try:
            return self._mapper
        except AttributeError:
            raise Exception('Attribute Must Be Set Exception')

    def _get_table(
        self,
        reference_name: Optional[str] = None
    ) -> Union[Table, Alias]:
        """
        If reference_name passed returns table or alias which has name
        equal to reference_name.
        First searches alias in self._usage_aliases by name.
        Second searched table which is related with self._table with
        relationship name as reference_name.
        """
        if type(reference_name) is str:
            aliases: Tuple[Optional[Alias]] = self._get_usage_aliases
            filtered_aliases: Tuple[Optional[Alias]] = tuple(
                filter(lambda alias: reference_name in alias.name, aliases))
            if filtered_aliases:
                return filtered_aliases[0]

            try:
                reference = getattr(self._get_mapper, reference_name)
                tables: List[Table] = reference.property.mapper.tables
                return tables[0]
            except (IndexError, AttributeError):
                raise Exception('Incorrect Reference Name Exception')

        if not self._table:
            return self._get_mapper.__table__

        return self._table

    @property
    def _get_first_pk_column_name(self) -> str:
        """
        If self._first_pk_column_name is not defined
        searches in mapper pk columns, sets to self._first_pk_column_name that column name and
        returns first of the columns name, e.g. id column name
        else returns self._first_pk_column_name
        """
        if self._first_pk_column_name is None:
            primary_key_columns = get_primary_keys(self._get_mapper)
            first_pk_column_name: str = next(iter(primary_key_columns))
            self._first_pk_column_name = first_pk_column_name

        return self._first_pk_column_name

    @property
    def _get_first_pk_column(self) -> Column:
        """
        Returns first pk column of self._mapper
        """
        first_pk_column_name = self._get_first_pk_column_name
        return getattr(self._get_mapper, first_pk_column_name)

    @property
    def _get_usage_mappers(self) -> Iterable[orm_models.ORMBaseModel]:
        if not self._usage_mappers:
            return [self._get_mapper]
        return self._usage_mappers

    @property
    def _get_usage_aliases(self) -> Tuple[Alias]:
        if not self._usage_aliases:
            return tuple()
        return self._usage_aliases

    def _get_column(
        self,
        name: str,
        reference_name: Optional[str] = None,
    ) -> Column:
        """
        Searched column with name in self._table if reference_name not passed,
        else searches it in passed table or alias from self._get_table object
        """
        table: Union[Table, Alias] = self._get_table(reference_name=reference_name)

        column = table.columns.get(name)
        if isinstance(column, Column):
            return column

        raise Exception('Column Does Not Exist Exception')

    @property
    def _get_select_stmt(self) -> Select:
        """
        Returns self._select_stmt if it's not None and defined in subclasses or
        returns select self._mapper
        """
        if self._select_stmt is not None:
            return self._select_stmt
        return select(self._get_mapper)

    @property
    def _get_single_record_adapter(self) -> Callable:
        try:
            return self._single_record_adapter
        except AttributeError:
            raise Exception('Attribute Must Be Set Exception')

    @property
    def _get_multiple_records_adapter(self) -> Callable:
        try:
            return self._multiple_records_adapter
        except AttributeError:
            raise Exception('Attribute Must Be Set Exception')

    @property
    def _get_sorting_columns(self) -> Tuple[str]:
        try:
            return self._sorting_columns
        except AttributeError:
            raise Exception('Attribute Must Be Set Exception')

    def __init__(
        self
    ):
        """
        Initializes provider object and bind it Filters object
        """
        self.session = async_session
        self._filters = self.Filters()
        self._filters._mapper = self._get_mapper
        self._filters._table = self._get_table()
        self._filters._joined_aliases = self._get_usage_aliases

    def _bind_order_limit_offset_to_stmt(
        self,
        select_stmt: Select,
        order_by: str = ...,
        order_reversed: bool = ...,
        limit: int = ...,
        offset: int = ...,
    ) -> Select:
        """
        Binds to passed select_stmt order_by, limit and offset statements
        and returns select_stmt
        """
        if type(order_by) == str and order_by in self._get_sorting_columns:
            column, reference_name = order_by, None
            if '.' in order_by:
                reference_name, column = order_by.split('.')
            by_column = self._get_column(column, reference_name)
            if type(order_reversed) == bool:
                by_column = by_column.desc() if order_reversed else by_column.asc()
            select_stmt = select_stmt.order_by(nullslast(by_column))

        if type(limit) == int:
            select_stmt = select_stmt.limit(limit)
        if type(offset) == int:
            select_stmt = select_stmt.offset(offset)

        return select_stmt

    def _make_select_stmt(
        self,
        select_stmt: Select = None,
        order_by: str = None,
        order_reversed: bool = None,
        limit: int = None,
        offset: int = None,
        filters: Union[Mapping, List] = {}
    ) -> Select:
        """
        Builds select statement by passed filters and return instance of Select class
        """
        filters = clear_from_ellipsis(filters)

        stmt = select_stmt
        if stmt is None:
            stmt = self._select_stmt
        if stmt is None:
            stmt = select(self._get_mapper)

        stmt = self._bind_order_limit_offset_to_stmt(
            select_stmt=stmt,
            order_by=order_by,
            order_reversed=order_reversed,
            limit=limit,
            offset=offset,
        )

        where_clause = self._filters.build_where_clause(filters=filters)
        stmt = stmt.where(where_clause)

        return stmt

    def _form_returning_stmt(
        self,
        stmt: Union[Insert, Update]
    ) -> Union[Insert, Update]:
        """
        Adds returning statement to insert or update statement which will return mapper first pk value
        """
        first_pk_column = self._get_first_pk_column
        return stmt.returning(first_pk_column)

    def _base_update_stmt(
        self,
        filters = {},
        values = {}
    ) -> Union[Update, Select]:
        """
        Builds necessary statement for using it in update methods
        """
        update_stmt = self._update_stmt
        if not update_stmt:
            update_stmt = update(self._get_mapper)

        where_clause = self._filters.build_where_clause(filters=filters)
        update_stmt = update_stmt.values(**values)
        update_stmt = update_stmt.where(where_clause)

        update_stmt = self._form_returning_stmt(stmt=update_stmt)

        return update_stmt

    async def _do_select(
        self,
        order_by: str = None,
        order_reversed: bool = None,
        limit: int = None,
        offset: int = None,
        filters: Union[Mapping, List] = {}
    ):
        """
        Executes built select stmt in self.session and returns answer
        """
        stmt = self._make_select_stmt(
            order_by=order_by,
            order_reversed=order_reversed,
            limit=limit,
            offset=offset,
            filters=filters
        )

        return (await self.session.execute(stmt)).all()

    async def _do_select_count(
        self,
        filters: Union[Mapping, List] = {}
    ) -> int:
        """
        Executing build select count stmt in self.session and
        return answer
        """
        stmt = self._select_count_stmt
        if stmt is None:
            stmt = select(func.count(distinct(self._get_first_pk_column))).select_from(self._get_mapper)

        where_clause = self._filters.build_where_clause(filters=filters)
        stmt = stmt.where(where_clause)

        return await self.session.scalar(stmt)

    async def _do_get(
        self,
        filters: Union[Mapping, List] = {}
    ):
        """
        """
        stmt = self._select_stmt
        if stmt is None:
            stmt = select(self._get_mapper)
        where_clause = self._filters.build_where_clause(filters=filters)
        stmt = stmt.where(where_clause)

        return (await self.session.execute(stmt)).first()

    async def _do_insert(
        self,
        **values
    ) -> Union[str, int]:
        """
        Does insert and returns value of first pk column in table
        """
        insert_stmt = self._insert_stmt
        if insert_stmt is None:
            insert_stmt = insert(self._get_mapper)

        insert_stmt = insert_stmt.values(**values)

        insert_stmt = self._form_returning_stmt(stmt=insert_stmt)
        result = await self.session.scalar(insert_stmt)
        await self.session.commit()
        return result

    async def _do_bulk_insert(
        self,
        VT: Tuple[Mapping[str, Any]],
    ) -> List[Union[str, int]]:
        """
        Does bulk inserts to table and returns first pk column values of each inserted rows
        """
        insert_stmt = self._insert_stmt
        if not insert_stmt:
            insert_stmt = insert(self._get_mapper)

        insert_stmt = insert_stmt.values(VT)

        insert_stmt = self._form_returning_stmt(stmt=insert_stmt)

        result = await self.session.scalar(insert_stmt)
        await self.session.commit()
        return result

    async def _do_update(
        self,
        filters,
        values
    ) -> Union[int, str]:
        """
        This method expects only one row to update and returns the row if this necessary
        """
        stmt = self._base_update_stmt(filters, values)

        # something went wrong, we couldn't find any solutions then `execution_options={"synchronize_session": False}`
        # see more in https://stackoverflow.com/questions/51221686/sqlalchemy-cannot-evaluate-binaryexpression-with-operator

        result = await self.session.scalar(stmt, execution_options={"synchronize_session": False})
        await self.session.commit()
        return result

    async def _do_bulk_update(
        self,
        filters,
        values
    ) -> List[Union[int, str]]:
        """
        This method expects multiple rows to update and returns the rows if this necessary
        """
        stmt = self._base_update_stmt(filters, values)

        # something went wrong, we couldn't find any solutions then `execution_options={"synchronize_session": False}`
        # see more in https://stackoverflow.com/questions/51221686/sqlalchemy-cannot-evaluate-binaryexpression-with-operator

        result = await self.session.scalar(stmt, execution_options={"synchronize_session": False})
        await self.session.commit()
        return result

    async def _do_delete(
        self,
        filters: Union[Mapping, List] = {}
    ) -> None:
        """
        """
        stmt = self._delete_stmt
        if stmt is None:
            stmt = delete(self._get_mapper)

        where_clause = self._filters.build_where_clause(filters=filters)
        stmt = stmt.where(where_clause)

        # something went wrong, we couldn't find any solutions then `execution_options={"synchronize_session": False}`
        # see more in https://stackoverflow.com/questions/51221686/sqlalchemy-cannot-evaluate-binaryexpression-with-operator
        await self.session.execute(stmt, execution_options={"synchronize_session": False})

    async def select(
        self,
        order_by: str = None,
        order_reversed: bool = None,
        limit: int = None,
        offset: int = None,
        filters: Union[Mapping, List] = {}
    ):
        """
        """
        filters = clear_from_ellipsis(filters)

        records = await self._do_select(
            order_by=order_by,
            order_reversed=order_reversed,
            limit=limit,
            offset=offset,
            filters=filters
        )

        return await self._get_multiple_records_adapter(records)

    async def select_count(
        self,
        filters: Union[Mapping, List] = {}
    ) -> int:
        """
        """
        filters = clear_from_ellipsis(filters)

        return await self._do_select_count(filters=filters)

    async def select_rows(
        self,
        order_by: str = ...,
        order_reversed: bool = ...,
        filters: Union[Mapping, List] = {}
    ) -> List[Tuple[Any]]:
        """
        Returns list of tuple where tuple contains only rows which were included to filters
        """
        select_columns: List[Column] = []
        for lookup, value in filters.items():
            column_name, *_ = lookup.split(self._filters.LOOKUP_STRING)
            select_columns.append(self._get_column(column_name))
        where_clause = self._filters.build_where_clause(filters=filters)
        stmt = select(*select_columns).where(where_clause)

        if type(order_by) == str and order_by in self._get_sorting_columns:
            by_column = self._get_column(order_by)
            if type(order_reversed) == bool:
                by_column = by_column.desc() if order_reversed else by_column.asc()
            stmt = stmt.order_by(by_column)

        return (await self.session.execute(stmt)).all()

    async def get(
        self,
        filters: Union[Mapping, List] = {}
    ):
        """
        """
        filters = clear_from_ellipsis(filters)

        if not filters:
            raise Exception('Filters Must Be Passed Exception')

        record = await self._do_get(filters=filters)

        if not record:
            raise Exception(self._does_not_exist_exception)

        return await self._get_single_record_adapter(*record)

    async def get_row(
        self,
        filters: Union[Mapping, List] = {}
    ) -> Tuple[Any]:
        """
        Returns tuple contains only rows which were included to filters
        """
        select_columns: List[Column] = []
        for lookup, value in filters.items():
            column_name, *_ = lookup.split(self._filters.LOOKUP_STRING)
            select_columns.append(self._get_column(column_name))
        where_clause = self._filters.build_where_clause(filters=filters)
        stmt = select(*select_columns).where(where_clause)
        return (await self.session.execute(stmt)).first()

    async def insert(
        self,
        **values
    ):
        """
        Makes insert and returns self.get
        """
        values = clear_from_ellipsis(values)

        first_pk_column_name: str = self._get_first_pk_column_name
        record_pk_value: Union[int, str] = await self._do_insert(**values)

        return await self.get(
            filters={first_pk_column_name + '__e': record_pk_value}
        )

    async def bulk_insert(
        self,
        VT: Tuple[Dict[str, Any]]
    ):
        """
        Make bulk insert and returns self.select result
        """
        first_pk_column_name: str = self._get_first_pk_column_name
        records_pk_values: List[Union[int, str]] = await self._do_bulk_insert(VT=VT)

        return await self.select(
            filters={
                first_pk_column_name + AlchemyFilters.LOOKUP_STRING + AlchemyFilters.IN_OPERATOR: records_pk_values
            }
        )

    async def get_or_insert(
        self,
        **values
    ):
        """
        Can accept only values with column which are not unique or pk,
        Tries to find row table with passed values params if such row does not exist
        then insert new row with passed values params
        """
        values = clear_from_ellipsis(values)
        for column_name, value in values.items():
            column: Column = self._get_column(column_name)
            if column.unique:
                raise Exception('Column Is Unique Exception')

        try:
            return await self.get(filters={**values})
        except:
            return await self.insert(**values)

    async def update(
        self,
        filters: Union[Mapping, Dict] = {},
        **kwargs,
    ):
        """
        All keys in kwargs which contains self._filters.LOOKUP_STRING is
        used as filters, rest used as values in update query.
        So kwargs = {'name__e': 'some_name', 'name': 'new_some_name'}
        here 'name__e' used build where clause and 'name' used to set value to
        name column
        """
        kwargs = clear_from_ellipsis(kwargs)
        filters = clear_from_ellipsis(filters)
        # Separate filters and values from kwargs,
        # so filters is string that contains LOOKUP_STRING
        # and values is regular string
        # that does not contain LOOKUP_STRING
        values: Dict[str, Any] = dict()
        for key, value in kwargs.items():
            if self._filters.LOOKUP_STRING in key:
                filters[key] = value
            else:
                values[key] = value

        if not filters:
            raise Exception('Filters Must Be Passed Exception')

        if not values:
            return await self.get(filters=filters)

        first_pk_column_name: str = self._get_first_pk_column_name
        record_pk_value: Union[int, str] = await self._do_update(filters, values)

        return await self.get(
            filters={ first_pk_column_name: record_pk_value }
        )

    async def bulk_update(
        self,
        filters: Union[Mapping, Dict] = {},
        **kwargs
    ):
        """
        All keys in kwargs which contains self._filters.LOOKUP_STRING is
        used as filters, rest used as values in update query.
        So kwargs = {'name__e': 'some_name', 'name': 'new_some_name'}
        here 'name__e' used build where clause and 'name' used to set value to
        name column
        """
        kwargs = clear_from_ellipsis(kwargs)
        filters = clear_from_ellipsis(filters)

        # Separate filters and values from kwargs,
        # so filters is string that contains LOOKUP_STRING
        # and values is regular string
        # that does not contain LOOKUP_STRING
        values: Dict[str, Any] = dict()
        for key, value in kwargs.items():
            if self._filters.LOOKUP_STRING in key:
                filters[key] = value
            else:
                values[key] = value

        if not filters:
            raise Exception('Filters Must Be Passed Exception')

        first_pk_column_name: str = self._get_first_pk_column_name
        records_pk_values: List[Union[int, str]] = await self._do_bulk_update(filters, values)

        return await self.select(
            filters={
                first_pk_column_name + AlchemyFilters.LOOKUP_STRING + AlchemyFilters.IN_OPERATOR: records_pk_values
            }
        )

    async def update_or_insert(
        self,
        **kwargs
    ):
        """
        Keys with LOOKUP FILTER perceived as filter params to find rows that satisfied passed filters
        and tries to update them columns that was passed in kwargs without LOOKUP FILTER
        """
        # Separate filters and values from kwargs,
        # so filters is string that contains LOOKUP_STRING
        # and values is regular string
        # that does not contain LOOKUP_STRING
        kwargs = clear_from_ellipsis(kwargs)

        filters: Dict[str, Any] = dict()
        values: Dict[str, Any] = dict()
        for key, value in kwargs.items():
            if self._filters.LOOKUP_STRING in key:
                filters[key] = value
            else:
                values[key] = value
                column: Column = self._get_column(key)
                if column.unique:
                    raise Exception('Column Is Unique Exception')

        if not filters:
            raise Exception('Filters Must Be Passed Exception')

        try:
            return await self.update(**kwargs)
        except:
            return await self.insert(**values)

    async def delete(
        self,
        filters: Union[Mapping, List] = {}
    ) -> None:
        """
        Delete all rows from table that satisfies to filters
        """
        filters = clear_from_ellipsis(filters)
        # If not filters raise exception
        if not filters:
            raise Exception('Filters Must Be Passed Exception')

        await self._do_delete(filters=filters)

    async def bulk_delete(
        self,
        filters: Union[Mapping, List] = {}
    ) -> None:
        """
        Delete all rows from table that satisfies to filters
        """
        return await self.delete(filters=filters)
