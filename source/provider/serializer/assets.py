from typing import List, Tuple

from source.service import domain
from source.provider import models as orm_models


async def record_to_assets(
    record: orm_models.Assets
) -> domain.Assets:
    assets = domain.Assets(
        tg_id=record.tg_id,
        assets=record.assets,
        assets_type=record.type
    )
    return assets


async def records_to_assets(
    records: List[Tuple[orm_models.Assets]]
) -> domain.AssetsList:
    assets_list = domain.AssetsList()
    for record in records:
        assets_list.items.append(await record_to_assets(*record))

    return assets_list


async def data_to_crypto_info(response: dict) -> domain.CryptoInfo:
    crypto_info = domain.CryptoInfo(
        name=response['name'],
        symbol=response['symbol'],
        price=response['market_data']['current_price']['usd']
    )
    return crypto_info
