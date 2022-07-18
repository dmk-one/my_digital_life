from aiogram import types
from aiogram.dispatcher import FSMContext


async def cancel_state(
    mess: types.Message,
    state: FSMContext
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
