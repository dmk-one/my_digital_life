import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


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


# async def cancel_handler(
#     *args,
#     state: FSMContext
# ):
#     await state.finish()
