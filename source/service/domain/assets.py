from typing import List, Optional
from pydantic import BaseModel


class Assets(BaseModel):
    tg_id: int
    assets: Optional[dict]


class AssetsList(BaseModel):
    items: List[Assets] = []
