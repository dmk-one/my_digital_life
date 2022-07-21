from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel


class AssetsTypes(IntEnum):
    CRYPTO = 0
    STOCK = 1
    OTHER = 2


class Assets(BaseModel):
    tg_id: int
    assets: Optional[dict]
    assets_type: AssetsTypes


class AssetsList(BaseModel):
    items: List[Assets] = []


class CryptoInfo(BaseModel):
    name: str
    symbol: str
    price: float
