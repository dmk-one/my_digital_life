from aiogram.utils import executor
from bot import dispatcher
import registrator


async def on_start(_):
    print('BOT STARTED !!!')


registrator.register_admin_handlers(dispatcher=dispatcher)
registrator.register_customer_handlers(dispatcher=dispatcher)
registrator.register_handlers_without_param(dispatcher=dispatcher)


executor.start_polling(
    dispatcher=dispatcher,
    skip_updates=True,
    on_startup=on_start
)
