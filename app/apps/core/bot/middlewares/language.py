from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any, Union
from aiogram.types import Update, user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.translater import Translator


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], 
        event: Update, 
        data: Dict[str, Any]
    ) -> Any:
        telegram_user: Union[user.User, None] = data.get('event_from_user')
        await Translator.set_locale(telegram_user.language_code)
        return await handler(event, data)