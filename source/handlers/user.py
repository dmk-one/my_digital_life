from aiogram import types
from keyboards import keyb
from source.service.user import UserService


service = UserService()


async def get_keyboards(
    mess: types.Message
):
    await mess.answer('Keyboards activated!', reply_markup=keyb)


async def add_user_phone(
    mess: types.Message
):
    await service.add_user_phone(
        tg_id=mess.from_user.id,
        phone_number=mess.contact.phone_number
    )
    await mess.answer('Номер добавлен')


async def return_message(
    mess: types.Message
):
    await mess.answer(f'Your message: {mess.text}')


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
