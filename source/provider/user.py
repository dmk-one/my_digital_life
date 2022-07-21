from .base import BaseAlchemyModelProvider
from . import serializer
from . import models as orm_models


class UsersProvider(BaseAlchemyModelProvider):

    _mapper = orm_models.Users

    _sorting_columns = ('id', 'username', 'tg_id', 'first_name')

    _single_record_adapter = staticmethod(serializer.record_to_users)
    _multiple_records_adapter = staticmethod(serializer.records_to_users)
