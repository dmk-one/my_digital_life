from typing import List, Tuple

from source.service import domain
from source.provider import models as orm_models


async def record_to_users(record: orm_models.Users) -> domain.Users:
    user = domain.Users(
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


async def records_to_users(records: List[Tuple[orm_models.Users]]) -> domain.UserList:
    user_list = domain.UserList()
    for record in records:
        user_list.items.append(await record_to_users(*record))

    return user_list
