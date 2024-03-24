import aiogram.types
from app.apps.core.DTO import SearchTelegramAccount
import typing
from asgiref.sync import sync_to_async
from app.apps.core.models import SearchTelegramUser
from app.apps.core.repositories.base import BaseRepository


colors = {
    'yellow': 'желтый',
    'red': 'красный',
    'black': 'черный',
}


class SearchTelehramUserRepository(BaseRepository):
    @sync_to_async
    def get(self: None, **filters) -> SearchTelegramUser:
        return super().to_list(SearchTelegramUser.objects.filter(**filters).all())

    @sync_to_async
    def findFree(with_dto=True, **filters):
        user = SearchTelegramUser.objects.filter(
            **(filters | {'is_free': True})).first()

        if with_dto:
            return SearchTelegramAccount(user)

        return user
