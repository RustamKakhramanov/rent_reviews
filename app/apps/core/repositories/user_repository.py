from typing import Final
from asgiref.sync import sync_to_async, async_to_sync
from app.apps.core.models import TariffPlan, TelegramUser
from aiogram.types import Message
from app.apps.core.DTO import TariffDto
from app.apps.core.repositories.base import BaseRepository
from app.apps.core.bot.enum import UserRole


class UserRepository:
    message: Message

    @sync_to_async
    def save(self: None, data: dict) -> tuple[TelegramUser, bool]:
        return TelegramUser.objects.get_or_create(
            telegram_id=data['telegram_id'],
            telegram_username=data['telegram_username'],
            telegram_name=data['telegram_name'],
        )

    @sync_to_async
    def save_and_set_tariff(self: None, data: dict, tariff: TariffPlan | None = None, get_entities: bool | None = None):
        user = TelegramUser.objects.filter(
            telegram_id=data['telegram_id']).first()

        if (not user):
            user = TelegramUser(telegram_id=data['telegram_id'])
            
        if (not tariff):
            tariff = TariffPlan.objects.filter(is_default=True).first()

        user.telegram_username = data['telegram_username']
        user.telegram_name = data['telegram_name']
        user.tariff_plan = tariff

        try:
            user.save()
            if get_entities:
                return [user, tariff]
            return True
        except Exception:
            return False

    @sync_to_async
    def set_tariff(self: None,  user:TelegramUser, tariff: TariffPlan | None = None, get_entities: bool = False):
        if (not tariff):
            tariff = TariffPlan.objects.filter(is_default=True).first()

        try:
            user.tariff_plan = tariff
            user.save()
            if get_entities:
                return [user, tariff]
            return True
        except Exception:
            return False

    @sync_to_async
    def update(self: None, id, **kwargs: any) -> tuple[TelegramUser, bool]:
        return TelegramUser.objects.filter(telegram_id=id).update(**kwargs)

    @sync_to_async
    def fin_and_update(self: None, id, **kwargs: any) -> tuple[TelegramUser, bool]:
        result = TelegramUser.objects.filter(telegram_id=id).update(**kwargs)
        if (result):
            return TelegramUser.objects.filter(telegram_id=id).first()
        return False

    @sync_to_async
    def find(self: None, id: int) -> tuple[TelegramUser, bool, None]:
        return TelegramUser.objects.filter(telegram_id=id).first()
    @sync_to_async
    def get_admins(self: None) -> tuple[TelegramUser, bool, None]:
        return BaseRepository().to_list(TelegramUser.objects.filter(role=UserRole.ADMIN.value).all())

    @sync_to_async
    def exists(self: None, id: int) -> tuple[TelegramUser, bool, None]:
        return TelegramUser.objects.filter(telegram_id=id).exists()

    def check_username(name: str) -> bool:
        if isinstance(name, str) and 3 < len(name) < 12 and name[0].isalpha():
            return True
        return False

    @sync_to_async
    def get_tariff(self: None, id: int):
        user = TelegramUser.objects.filter(telegram_id=id).first()
        
        return user.tariff_plan
    
    #TODO Calculate tariff
    @sync_to_async
    def get_permited_tariff(self: None, user_or_id: int|TelegramUser, with_dto=True)-> TariffDto:
        if not isinstance(user_or_id, TelegramUser):
            user = TelegramUser.objects.filter(telegram_id=user_or_id).first()
        else:
            user = user_or_id
            
        if(user):
            if with_dto:
                return TariffDto(user.tariff_plan)
            
            return user.tariff_plan
        else:
            return None
        
        
        
    @sync_to_async
    def get_allowed_chats(self: None, id: int):
        user = TelegramUser.objects.filter(telegram_id=id).first()
        
        return int(user.tariff_plan.group_quantity)

    @sync_to_async
    def deleteAll(self: None):
        return TelegramUser.objects.all().delete()
