from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
token = '5412968943:AAHaTvwTRVijhtwlNcEOpMDXKyxehSvsrHo'

bot = Bot(token=token)
dispatcher = Dispatcher(bot, storage=storage)
