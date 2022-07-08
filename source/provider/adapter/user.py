from typing import List, Tuple

from source.service import domain
from source.provider import models as orm_models


async def record_to_user(record: orm_models.User) -> domain.User:
    print('\nRECORD ARTTRS')
    print(record.tg_id)
    print(record.username)
    print(record.first_name)
    print(record.last_name)
    print(record.is_bot)
    print(record.language_code)
    print(record.is_superuser)
    print(record.added_to_attachment_menu)
    print(record.can_join_groups)
    print(record.can_read_all_group_messages)
    print(record.supports_inline_queries)
    print(record.last_activity)
    print(record.registration_date)
    print(record.phone_number)
    user = domain.User(
        tg_id=record.tg_id,
        username=record.username,
        first_name=record.first_name,
        last_name=record.last_name,
        is_bot=record.is_bot,
        language_code=record.language_code,
        is_superuser=record.is_superuser,
        added_to_attachment_menu=record.added_to_attachment_menu,
        can_join_groups=record.can_join_groups,
        can_read_all_group_messages=record.can_read_all_group_messages,
        supports_inline_queries=record.supports_inline_queries,
        last_activity=record.last_activity,
        registration_date=record.registration_date,
        phone_number=record.phone_number
    )
    return user


async def records_to_users(records: List[Tuple[orm_models.User]]) -> domain.UserList:
    user_list = domain.UserList()
    for record in records:
        user_list.items.append(await record_to_user(*record))

    return user_list
