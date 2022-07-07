import requests
from aiogram import types
from keyboards import keyb


async def get_keyboards(
    mess: types.Message
):
    await mess.answer('Keyboards activated!', reply_markup=keyb)


async def get_btc_price(
    mess: types.Message
):
    response = requests.get('https://coinmarketcap.com/currencies/bitcoin/')

    first_index = response.text.find('\\"p\\"')
    last_index = response.text.find(',\\"p1h\\"')

    price = float(response.text[first_index+6:last_index])

    await mess.answer(f'BTC price: {round(price, 2)} $')


async def phone(
    mess: types.Message
):
    print(mess)
    await mess.answer(f'-----')


async def get_eth_price(
    mess: types.Message
):
    response = requests.get('https://coinmarketcap.com/currencies/ethereum/')

    first_index = response.text.find('\\"p\\"')
    last_index = response.text.find(',\\"p1h\\"')

    price = float(response.text[first_index+6:last_index])

    await mess.answer(f'ETH price: {round(price, 2)} $')


async def return_message(
    mess: types.Message
):
    print(mess.contact.phone_number)
    await mess.answer(f'Your message: {mess.text}')
