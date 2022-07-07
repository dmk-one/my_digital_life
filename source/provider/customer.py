from typing import Iterable, Union, Mapping, List
from sqlalchemy.sql import select, Select
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import BinaryExpression
from service.exception import (
    CustomerDoesNotExist,
    LookupOperatorNotFoundException
)
from service import domain
from .base import BaseAlchemyModelProvider
from .adapter.customer import record_to_customer, records_to_customers
from . import models as orm_models
from .shared.utils import clear_from_ellipsis


class CustomerProvider(BaseAlchemyModelProvider):
    """
    >>> select(filters = {
    >>>     "name__ilike": "%S%"
    >>> })
    >>> SELECT ami_customer.id, ami_customer.uuid, ami_customer.name,
    >>>     ami_customer.email, ami_customer.description, ami_customer.type,
    >>>     ami_customer.team, ami_customer.first_name, ami_customer.last_name,
    >>>     ami_customer.password, ami_customer.is_active, ami_customer.is_superuser,
    >>>     ami_customer.last_activity, ami_customer.date_joined, ami_customer.parent_id
    >>> FROM ami_customer
    >>> WHERE ami_customer.name ILIKE lower('%S%')
    """

    _mapper = orm_models.Customer

    _sorting_columns = ('id', 'uuid', 'email', 'name')

    _single_record_adapter = staticmethod(record_to_customer)
    _multiple_records_adapter = staticmethod(records_to_customers)

    _does_not_exist_exception = CustomerDoesNotExist