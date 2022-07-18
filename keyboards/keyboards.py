from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# Main menu
my_assets = KeyboardButton('/my_assets')
crypto_price = KeyboardButton('/crypto_price')

# Assets keyboards
crypto_assets = KeyboardButton('/crypto_assets')
other_assets = KeyboardButton('/other_assets')

# User's keyboards
share_num = KeyboardButton('/share_num', request_contact=True)
where_am_i = KeyboardButton('/where_am_i', request_location=True)


main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
assets = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

main_menu.add(my_assets).add(crypto_price)
assets.row(crypto_assets, other_assets)
user.row(share_num, where_am_i)
