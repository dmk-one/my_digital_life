import requests
from aiogram import types
from keyboards import keyb


async def get_keyboards(
    mess: types.Message
):
    await mess.answer('Keyboards activated!', reply_markup=keyb)


# async def get_btc_price(
#     mess: types.Message
# ):
#     response = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
#
#     first_index = response.text.find('\\"p\\"')
#     last_index = response.text.find(',\\"p1h\\"')
#
#     price = float(response.text[first_index+6:last_index])
#
#     await mess.answer(f'BTC price: {round(price, 2)} $')


async def phone(
    mess: types.Message
):
    await mess.answer(f'-----')




async def return_message(
    mess: types.Message
):
    await mess.answer(f'Your message: {mess.text}')
