from typing import Optional, Union

import requests

from source.service import domain
from source.provider.assets import AssetsProvider
from source.provider.serializer import data_to_crypto_info
from source.provider.exception import AssetAlreadyExist, AssetNameIncorrect


class AssetsService:

    _provider: AssetsProvider

    def __init__(self):
        self._provider = AssetsProvider()

    async def get_crypto_info(
        self,
        crypto_name: str
    ) -> Union[domain.CryptoInfo, AssetNameIncorrect]:
        try:
            url = f'https://api.coingecko.com/api/v3/coins/{crypto_name}'
            response = requests.get(url).json()
            crypto_info = await data_to_crypto_info(response)
        except KeyError:
            return AssetNameIncorrect()

        return crypto_info

    async def get_crypto_assets(
        self,
        tg_id: int
    ) -> domain.Assets:

        return await self._provider.get(
            filters={
                'tg_id': tg_id,
                'type': domain.AssetsTypes.CRYPTO.value
            }
        )

    async def add_crypto_asset(
        self,
        tg_id: int,
        crypto_name: str,
        value: float
    ) -> Union[domain.Assets, AssetAlreadyExist, AssetNameIncorrect]:

        assets = await self.get_crypto_assets(tg_id=tg_id)
        if assets.assets.get(crypto_name):
            return AssetAlreadyExist()

        crypto_info = await self.get_crypto_info(crypto_name=crypto_name)
        if type(crypto_info) is AssetNameIncorrect:
            return AssetNameIncorrect()

        assets.assets[crypto_name] = value
        new_assets = await self._provider.update(
            assets=assets.assets,
            filters={
                'tg_id': tg_id,
                'type': domain.AssetsTypes.CRYPTO.value
            }
        )
        return new_assets

    async def create(
        self,
        tg_id: int
    ):

        await self._provider.insert(
            tg_id=tg_id,
            type=domain.AssetsTypes.CRYPTO.value,
            assets={}
        )

        await self._provider.insert(
            tg_id=tg_id,
            type=domain.AssetsTypes.STOCK.value,
            assets={}
        )

        await self._provider.insert(
            tg_id=tg_id,
            type=domain.AssetsTypes.OTHER.value,
            assets={}
        )
