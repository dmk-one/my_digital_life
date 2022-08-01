from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import assets_menu, crypto_assets_menu
from source.service.assets import AssetsService


service = AssetsService()


class FSMGetCryptoPrice(StatesGroup):
    crypto_name = State()


class FSMAddCryptoAsset(StatesGroup):
    crypto_name = State()
    value = State()


class FSMEditCryptoAsset(StatesGroup):
    crypto_name = State()
    value = State()


# ----------- ASSETS MENU HANDLERS ----------- #

async def get_assets_menu(
    mess: types.Message
):
    await mess.answer('Меню активов:', reply_markup=assets_menu)


async def get_crypto_assets_menu(
    mess: types.Message
):
    await mess.answer('Меню крипто активов:', reply_markup=crypto_assets_menu)


# ----------- CRYPTO ASSETS HANDLERS WITHOUT STATES ----------- #

async def get_crypto_assets(
    mess: types.Message
):
    assets = await service.get_crypto_assets(mess.from_user.id)
    await mess.answer('Мои активы:')
    for crypto_name, value in assets.assets.items():
        await mess.answer(f'{crypto_name} - {value}')


# ----------- CRYPTO ASSETS HANDLERS WITH STATES ----------- #

async def get_crypto_price_state_starter(
    mess: types.Message
):
    await FSMGetCryptoPrice.crypto_name.set()
    await mess.reply('Введите полное название криптовалюты (например: bitcoin)')


async def get_crypto_price(
    mess: types.Message,
    state: FSMContext
):
    crypto_info = await service.get_crypto_info(crypto_name=mess.text.lower())
    if crypto_info is None:
        await mess.answer('Ошибка, проверьте название монетки (например: bitcoin)')
        await state.finish()
        return crypto_info
    await mess.answer(f'Текущая цена {crypto_info.name}: {crypto_info.price}')
    await state.finish()


async def add_crypto_asset_state_starter(
    mess: types.Message
):
    await FSMAddCryptoAsset.crypto_name.set()
    await mess.reply('Введите полное название криптовалюты которую '
                     'хотите добавить в портфель(например: bitcoin)')


async def add_crypto_asset(
    mess: types.Message,
    data: dict
):
    await service.add_crypto_asset(
        tg_id=mess.from_user.id,
        crypto_name=data['crypto_name'],
        value=data['value']
    )
    await get_crypto_assets(mess=mess)


async def state_crypto_asset_name(
    mess: types.Message,
    state: FSMContext
):
    await state.update_data(crypto_name=mess.text.lower())

    await FSMAddCryptoAsset.value.set()
    await mess.reply(f'Введите количество {mess.text}')


async def state_crypto_asset_value(
    mess: types.Message,
    state: FSMContext
):
    await state.update_data(value=int(mess.text.lower()))

    data = await state.get_data()

    await add_crypto_asset(
        mess=mess,
        data=data
    )

    await state.finish()


async def edit_crypto_asset_state_starter(
    mess: types.Message
):
    await FSMEditCryptoAsset.crypto_name.set()
    await mess.reply('Введите полное название криптовалюты в портфеле которую'
                     'хотите редактировать (например: bitcoin)')


async def edit_crypto_asset(
    mess: types.Message,
    data: dict
):
    await service.update_crypto_asset(
        tg_id=mess.from_user.id,
        crypto_name=data['crypto_name'],
        value=data['value']
    )
    await get_crypto_assets(mess=mess)


async def state_crypto_asset_name(
    mess: types.Message,
    state: FSMContext
):
    await state.update_data(crypto_name=mess.text.lower())

    await FSMEditCryptoAsset.value.set()
    await mess.reply(f'Введите количество {mess.text}')


async def state_crypto_asset_value(
    mess: types.Message,
    state: FSMContext
):
    await state.update_data(value=int(mess.text.lower()))

    data = await state.get_data()

    await add_crypto_asset(
        mess=mess,
        data=data
    )

    await state.finish()
