from typing import Final
from asgiref.sync import sync_to_async
from app.apps.core.models import TariffPlan, TelegramUser
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.DTO import TariffDto


class TariffRepository:
    @sync_to_async
    def save(self: None, data: dict) -> tuple[TariffPlan, bool]:
        return TariffPlan.objects.create(
            name=data['name'],
            group_quantity=data['group_quantity'],
            keyword_quantity=data['keyword_quantity'],
            old_messages_offset=data['old_messages_offset'],
            daemon_hours_quantity=data['daemon_hours_quantity']
        )

    @sync_to_async
    def update(self: None, id, **kwargs: any) -> tuple[TariffPlan, bool]:
        return TariffPlan.objects.filter(telegram_id=id).update(**kwargs)

    @sync_to_async
    def fin_and_update(self: None, id, **kwargs: any) -> tuple[TariffPlan, bool]:
        result = TariffPlan.objects.filter(telegram_id=id).update(**kwargs)
        if (result):
            return TariffPlan.objects.filter(telegram_id=id).first()
        return False

    @sync_to_async
    def find(self: None, id: int) -> tuple[TariffPlan, bool, None]:
        return TariffPlan.objects.filter(telegram_id=id).first()

    @sync_to_async
    def exists(self: None, id: int) -> tuple[TariffPlan, bool, None]:
        return TariffPlan.objects.filter(telegram_id=id).exists()

    @sync_to_async
    def get_default(self: None) -> TariffPlan:
        return TariffPlan.objects.filter(is_default=True).first()

    @sync_to_async
    def attach_default_to_user(self: None, user: TelegramUser) -> TariffPlan:
        try:
            default = TariffPlan.objects.filter(is_default=True).first()
            user.tariff_plan = default
            user.save()
            return True
        except Exception:
            return False

    @sync_to_async
    def is_permited_for_user(self, user_id, key):
        user = TelegramUser.objects.filter(telegram_id=user_id).first()
        if (user and user.tariff_plan):
            tariff = TariffDto(user.tariff_plan)
            return int(tariff.__dict__[key])
        else:
            return None
