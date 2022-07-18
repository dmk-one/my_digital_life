from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot import bot


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()


admin_iset = [1299170162, ]


async def is_moderator_chat(
    mess: types.Message
):
    admin_id = mess.from_user.id
    await bot.send_message(admin_id, 'Your are moderator')
    await mess.delete()


async def is_admin(
    mess: types.Message
):
    if mess.from_user.id in admin_iset:
        await mess.reply('You are ADMIN')
    else:
        await mess.reply('You are standart user')


async def machine_state(
    mess: types.Message
):
    if mess.from_user.id in admin_iset:
        await FSMAdmin.photo.set()
        await mess.reply('ZAGRUZITE PLZ FOTKU')


async def load_photo(
    mess: types.Message,
    state: FSMContext
):
    if mess.from_user.id in admin_iset:
        async with state.proxy() as data:
            data['photo'] = mess.photo[0].file_id
        await FSMAdmin.next()
        await mess.reply('NAME VVEDITE PLZ')


async def load_name(
    mess: types.Message,
    state: FSMContext
):
    if mess.from_user.id in admin_iset:
        async with state.proxy() as data:
            data['name'] = mess.text
        async with state.proxy() as data:
            await mess.reply(f'PROXY: {str(data)}')
            await mess.reply(f'Success!')
        await state.finish()


# async def cancel_handler(
#     mess: types.Message,
#     state: FSMContext
# ):
#     if mess.from_user.id in admin_iset:
#         current_state = await state.get_state()
#         if current_state is None:
#             return
#         await state.finish()
#         await mess.reply('OK')



