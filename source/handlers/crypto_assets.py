from typing import Optional

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from source.service.assets import AssetsService
from .base_state import BaseCryptoFSM, FSMGetCryptoPrice, FSMAddCryptoAsset, FSMEditCryptoAsset


class CryptoPriceHandler:
    service = AssetsService()

    async def get_crypto_price_state_starter(
        self,
        mess: types.Message
    ):
        await FSMGetCryptoPrice.crypto_name.set()
        await mess.reply('Введите полное название криптовалюты (например: bitcoin)')

    async def get_crypto_price(
        self,
        mess: types.Message,
        state: FSMContext
    ):
        crypto_info = await self.service.get_crypto_info(crypto_name=mess.text.lower())
        if crypto_info is None:
            await mess.answer('Ошибка, проверьте название монетки (например: bitcoin)')
            await state.finish()
            return crypto_info
        await mess.answer(f'Текущая цена {crypto_info.name}: {crypto_info.price}')
        await state.finish()


class CryptoAssetHandler:
    service = AssetsService()

    async def get_assets(
        self,
        mess: types.Message
    ):
        assets = await self.service.get_crypto_assets(mess.from_user.id)
        await mess.answer('Мои активы:')
        for crypto_name, value in assets.assets.items():
            await mess.answer(f'{crypto_name} - {value}')

    async def add_asset(
        self,
        mess: types.Message,
        data: dict
    ):
        await self.service.add_crypto_asset(
            tg_id=mess.from_user.id,
            crypto_name=data['crypto_name'],
            value=data['value']
        )
        await self.get_assets(mess=mess)

    async def edit_asset(
        self,
        mess: types.Message,
        data: dict
    ):
        await self.service.update_crypto_asset(
            tg_id=mess.from_user.id,
            crypto_name=data['crypto_name'],
            value=data['value']
        )
        await self.get_assets(mess=mess)


class CryptoAssetStateHandler:

    service = AssetsService()

    command_fsm = {
        'add_crypto_asset': FSMAddCryptoAsset,
        'edit_crypto_asset': FSMEditCryptoAsset
    }

    current_fsm: Optional[BaseCryptoFSM] = None

    async def state_starter(
        self,
        mess: types.Message,
        command: Command.CommandObj
    ):
        fsm = self.command_fsm[command.command]
        self.current_fsm = fsm

        await fsm.crypto_name.set()
        await mess.reply(f'Введите полное название криптовалюты которую '
                         f'хотите {fsm.what_to_do}(например: bitcoin)')

    async def save_asset_name_in_state_data(
        self,
        mess: types.Message,
        state: FSMContext,
    ):
        await state.update_data(crypto_name=mess.text.lower())

        await self.current_fsm.value.set()
        await mess.reply(f'Введите количество {mess.text}')

    async def save_asset_value_in_state_data(
        self,
        mess: types.Message,
        state: FSMContext
    ):
        await state.update_data(value=int(mess.text.lower()))

        data = await state.get_data()

        await CryptoAssetHandler().add_asset(
            mess=mess,
            data=data
        )

        self.current_fsm = None
        await state.finish()
