from aiogram import types
from keyboards import keyb


async def start_bot(
    mess: types.Message
):
    await mess.answer('Hello!', reply_markup=keyb)