from source.service import domain
from source.provider.assets import AssetsProvider


class AssetsService:

    _provider: AssetsProvider

    def __init__(self):
        self._provider = AssetsProvider()

    async def get(
        self,
        tg_id: int = ...
    ) -> domain.Assets:

        return await self._provider.get(
            filters={
                'tg_id': tg_id
            }
        )