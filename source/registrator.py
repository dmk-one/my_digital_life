from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from source.handlers.cancel_state_handlers import cancel_state
from source.handlers.start import start_bot
from source.handlers.crypto import crypto_price, get_crypto_price, FSMCrypto
from source.handlers.user import get_keyboards, return_message, add_user_phone
from source.handlers.admin import machine_state, \
    load_name, load_photo, is_admin, is_moderator_chat, FSMAdmin


def register_start_handlers(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(start_bot, commands=['start', 'restart'])


def register_crypto_handlers(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(crypto_price, commands=['crypto_price'], state=None)
    dispatcher.register_message_handler(cancel_state, state='*', commands='cancel')
    dispatcher.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')
    dispatcher.register_message_handler(get_crypto_price, state=FSMCrypto.crypto_name)


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
    dispatcher.register_message_handler(get_keyboards, commands=['keyboards'])


def register_handlers_without_param(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(return_message)
