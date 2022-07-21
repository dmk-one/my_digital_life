from .base import BaseAlchemyModelProvider
from . import serializer
from . import models as orm_models


class AssetsProvider(BaseAlchemyModelProvider):

    _mapper = orm_models.Assets

    _sorting_columns = ('id', 'tg_id')

    _single_record_adapter = staticmethod(serializer.record_to_assets)
    _multiple_records_adapter = staticmethod(serializer.records_to_assets)
