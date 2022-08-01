from aiogram import types
from keyboards import assets_menu, crypto_assets_menu


async def get_assets_menu(
    mess: types.Message
):
    await mess.answer('Меню активов:', reply_markup=assets_menu)


async def get_crypto_assets_menu(
    mess: types.Message
):
    await mess.answer('Меню крипто активов:', reply_markup=crypto_assets_menu)
