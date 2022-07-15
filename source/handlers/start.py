from datetime import datetime

from aiogram import types
from source.service.user import UserService


_s_user = UserService()


async def start_bot(
    mess: types.Message
):
    user_name = mess.from_user.first_name + mess.from_user.last_name \
        if mess.from_user.last_name else mess.from_user.first_name

    try:
        # TODO update last_activity if exist
        await _s_user.get(
            tg_id=mess.from_user.id
        )

        await mess.answer(f'Welcome back {user_name}!!!')
    except:
        await _s_user.create(
            tg_id=mess.from_user.id,
            username=mess.from_user.username,
            first_name=mess.from_user.first_name,
            last_name=mess.from_user.last_name,
            is_bot=mess.from_user.is_bot,
            language_code=mess.from_user.language_code,
            added_to_attachment_menu=mess.from_user.added_to_attachment_menu,
            can_join_groups=mess.from_user.can_join_groups,
            can_read_all_group_messages=mess.from_user.can_read_all_group_messages,
            supports_inline_queries=mess.from_user.supports_inline_queries,
            is_superuser=False,
            last_activity=datetime.now(),
            registration_date=datetime.now()
        )

        await _s_user.get(
            tg_id=mess.from_user.id
        )

        await mess.answer(f'Hello {user_name}!!!')
