from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
token = ''

bot = Bot(token=token)
dispatcher = Dispatcher(bot, storage=storage)
