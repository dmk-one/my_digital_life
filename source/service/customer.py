import datetime
from typing import Union
from provider.customer import CustomerProvider


class CustomerService:

    _provider: CustomerProvider

    async def create(
        self,
        tg_id: int,
        username: str,
        first_name: str,
        is_bot: bool,
        language_code: str,
        is_superuser: bool,
        last_activity: datetime.datetime,
        registration_date: datetime.datetime,
        phone_number: int = ...
    ) -> domain.Customer:
