from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1 = KeyboardButton('/btc_price')
b2 = KeyboardButton('/eth_price')

b3 = KeyboardButton('share_num', request_contact=True)
b4 = KeyboardButton('where am i', request_location=True)

keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyb.add(b1).add(b2).row(b3, b4)
