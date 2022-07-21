from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# Main menu
my_assets = KeyboardButton('/my_assets')
crypto_price = KeyboardButton('/crypto_price')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu.add(my_assets).add(crypto_price)


# Assets menu
crypto_assets = KeyboardButton('/crypto_assets')
other_assets = KeyboardButton('/other_assets')

assets_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
assets_menu.row(crypto_assets, other_assets)


# Crypto Assets menu
show_crypto_assets = KeyboardButton('/show_crypto_assets')
add_crypto_assets = KeyboardButton('/add_crypto_asset')
edit_crypto_assets = KeyboardButton('/edit_crypto_asset')
delete_crypto_assets = KeyboardButton('/delete_crypto_asset')

crypto_assets_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
crypto_assets_menu.row(show_crypto_assets, add_crypto_assets)
crypto_assets_menu.row(edit_crypto_assets, delete_crypto_assets)


# User's keyboards
share_num = KeyboardButton('/share_num', request_contact=True)
where_am_i = KeyboardButton('/where_am_i', request_location=True)

user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user.row(share_num, where_am_i)
