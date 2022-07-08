from .base import BaseAlchemyModelProvider
from .adapter.user import record_to_user, records_to_users
from . import models as orm_models


class UserProvider(BaseAlchemyModelProvider):

    _mapper = orm_models.User

    _sorting_columns = ('id', 'uuid', 'email', 'name')

    _single_record_adapter = staticmethod(record_to_user)
    _multiple_records_adapter = staticmethod(records_to_users)
