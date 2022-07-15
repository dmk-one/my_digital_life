from .base import BaseAlchemyModelProvider
from .adapter.user import record_to_users, records_to_users
from . import models as orm_models


class UsersProvider(BaseAlchemyModelProvider):

    _mapper = orm_models.Users

    _sorting_columns = ('id', 'uuid', 'email', 'name')

    _single_record_adapter = staticmethod(record_to_users)
    _multiple_records_adapter = staticmethod(records_to_users)
