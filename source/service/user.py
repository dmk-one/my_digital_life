import datetime

from source.service import domain
from source.provider.user import UsersProvider


class UserService:

    _provider: UsersProvider

    def __init__(self):
        self._provider = UsersProvider()

    async def create(
        self,
        tg_id: int,
        username: str,
        first_name: str,
        last_name: str,
        is_bot: bool,
        language_code: str,
        added_to_attachment_menu: bool,
        can_join_groups: bool,
        can_read_all_group_messages: bool,
        supports_inline_queries: bool,
        is_superuser: bool,
        last_activity: datetime.datetime,
        registration_date: datetime.datetime,
        phone_number: int = ...
    ) -> domain.Users:

        user = await self._provider.insert(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_bot=is_bot,
            language_code=language_code,
            added_to_attachment_menu=added_to_attachment_menu,
            can_join_groups=can_join_groups,
            can_read_all_group_messages=can_read_all_group_messages,
            supports_inline_queries=supports_inline_queries,
            is_superuser=is_superuser,
            last_activity=last_activity,
            registration_date=registration_date,
            phone_number=phone_number
        )

        return user


    async def get(
        self,
        tg_id: int = ...,
        phone_number: int = ...
    ) -> domain.Users:

        return await self._provider.get(
            filters={
                'tg_id': tg_id,
                'phone_number': phone_number
            }
        )
