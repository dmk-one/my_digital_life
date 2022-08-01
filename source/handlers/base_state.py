from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseCryptoFSM(StatesGroup):
    crypto_name = State()
    value = State()
    what_to_do: str = ''


class FSMGetCryptoPrice(BaseCryptoFSM):
    ...


class FSMAddCryptoAsset(BaseCryptoFSM):
    crypto_name = State()
    what_to_do = 'добавить в портфель'


class FSMEditCryptoAsset(BaseCryptoFSM):
    crypto_name = State()
    what_to_do = 'редактировать в портфеле'


async def cancel_state(
    mess: types.Message,
    state: FSMContext
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


