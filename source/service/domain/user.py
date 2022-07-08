import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    tg_id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_bot: bool
    language_code: str
    added_to_attachment_menu: Optional[bool]
    can_join_groups: Optional[bool]
    can_read_all_group_messages: Optional[bool]
    supports_inline_queries: Optional[bool]
    is_superuser: bool
    last_activity: datetime.datetime
    registration_date: datetime.datetime
    phone_number: int = None


class UserList(BaseModel):
    items: List[User] = []
