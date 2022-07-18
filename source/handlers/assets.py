import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import assets
from source.service.assets import AssetsService


service = AssetsService()


class FSMCrypto(StatesGroup):
    crypto_name = State()


async def crypto_price(
    mess: types.Message
):
    await FSMCrypto.crypto_name.set()
    await mess.reply('Введите полное название криптовалюты (например: bitcoin)')


async def get_crypto_price(
    mess: types.Message,
    state: FSMContext
):
    try:
        url = f'https://api.coingecko.com/api/v3/coins/{mess.text.lower()}'
        response = requests.get(url).json()
        await mess.answer(response['market_data']['current_price']['usd'])
    except KeyError:
        await mess.answer('Ошибка, проверьте название монетки (например: bitcoin)')
    await state.finish()


async def get_assets_menu(
    mess: types.Message
):
    await mess.answer('Меню активов:', reply_markup=assets)


async def get_crypto_assets(
    mess: types.Message
):
    a = await service.get(mess.from_user.id)
    print(a)
    await mess.answer('Мои активы:')
    for crypto_ticker, value in a.assets.items():
        await mess.answer(f'{crypto_ticker} - {value}')
