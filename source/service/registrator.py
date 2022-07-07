from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from source.service import handlers, admin, FSMAdmin



def register_handlers_with_param(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(handlers.get_btc_price, commands=['eth_price'])
    dispatcher.register_message_handler(handlers.get_eth_price, commands=['eth_price'])
    dispatcher.register_message_handler(handlers.phone, commands=['share_num'])
    dispatcher.register_message_handler(handlers.get_keyboards, commands=['keyboards'])


def register_handlers_with_state(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(admin.machine_state, commands='Upload', state=None)

    dispatcher.register_message_handler(admin.cancel_handler, state='*', commands='cancel')
    dispatcher.register_message_handler(admin.cancel_handler, Text(equals='cancel', ignore_case=True), state='*')

    dispatcher.register_message_handler(admin.load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dispatcher.register_message_handler(admin.load_name, state=FSMAdmin.name)
    dispatcher.register_message_handler(admin.is_moderator_chat, commands=['am_i_moderator'], is_chat_admin=True)
    dispatcher.register_message_handler(admin.is_admin, commands=['am_i_admin'])


def register_handlers_without_param(
    dispatcher: Dispatcher
):
    dispatcher.register_message_handler(handlers.return_message, content_types= types.ContentTypes.CONTACT)
