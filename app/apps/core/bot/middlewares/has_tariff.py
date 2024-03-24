from aiogram import BaseMiddleware
import asgiref.sync
from typing import Callable, Awaitable, Dict, Any, Union
from aiogram.types import Update, user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.translater import Translator
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.models import TariffPlan, TelegramUser
from asgiref.sync import sync_to_async

class HasTariffMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], 
        event: Update, 
        data: Dict[str, Any]
    ) -> Any:
        # telegram_user: Union[user.User, None] = data.get('event_from_user')
        # db_user:TelegramUser = await UserRepository.find(telegram_user.id)
        
        # if db_user:
        #     tariff:TariffPlan = await UserRepository.get_permited_tariff(db_user)
        #     if not tariff.id:
        #         await UserRepository.set_tariff(db_user)
        
        return await handler(event, data)