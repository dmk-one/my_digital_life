from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from source.handlers.cancel_state_handlers import cancel_state
from source.handlers.start import start_bot
from source.handlers.assets import *
from source.handlers.user import get_main_menu_keyboards, return_message, add_user_phone
from source.handlers.admin import machine_state, \
    load_name, load_photo, is_admin, is_moderator_chat, FSMAdmin


def register_start_handlers(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(start_bot, commands=['start', 'restart'])


def register_assets_handlers(
    dispatcher: Dispatcher
):
    # ------------------ CRYPTO PRICE ------------------ #
    dispatcher.register_message_handler(get_crypto_price_state, commands=['crypto_price'], state=None)
    dispatcher.register_message_handler(cancel_state, state='*', commands='cancel')
    dispatcher.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')
    dispatcher.register_message_handler(get_crypto_price, state=FSMGetCryptoPrice.crypto_name)

    # ------------------ ADD CRYPTO ------------------ #
    dispatcher.register_message_handler(add_crypto_asset_state_starter, commands=['one'], state=None)
    dispatcher.register_message_handler(cancel_state, state='*', commands='cancel')
    dispatcher.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')
    dispatcher.register_message_handler(save_crypto_asset_name, state=FSMCryptoAsset.crypto_name)
    dispatcher.register_message_handler(save_crypto_asset_value, state=FSMCryptoAsset.value)
    dispatcher.register_message_handler(add_crypto_asset, state=FSMCryptoAsset.value)

    # ------------------ ASSETS MENU ------------------ #
    dispatcher.register_message_handler(get_assets_menu, commands=['my_assets'])
    dispatcher.register_message_handler(get_crypto_assets_menu, commands=['crypto_assets'])

    # ------------------ CRYPTO ASSETS MENU ------------------ #
    dispatcher.register_message_handler(get_crypto_assets, commands=['show_crypto_assets'])


def register_admin_handlers(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(machine_state, commands='Upload', state=None)

    dispatcher.register_message_handler(cancel_state, state='*', commands='cancel')
    dispatcher.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')

    dispatcher.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dispatcher.register_message_handler(load_name, state=FSMAdmin.name)
    dispatcher.register_message_handler(is_moderator_chat, commands=['am_i_moderator'], is_chat_admin=True)
    dispatcher.register_message_handler(is_admin, commands=['am_i_admin'])


def register_user_handlers(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(add_user_phone, content_types=types.ContentTypes.CONTACT)
    # dispatcher.register_message_handler(handlers.get_btc_price, commands=['eth_price'])
    # dispatcher.register_message_handler(handlers.phone, commands=['share_num'])
    dispatcher.register_message_handler(get_main_menu_keyboards, commands=['keyboards'])


def register_handlers_without_param(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(return_message)
