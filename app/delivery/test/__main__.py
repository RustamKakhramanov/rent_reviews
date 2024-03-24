import asyncio
from telethon import TelegramClient
from app.apps.core.repositories.search_telegram_user import SearchTelehramUserRepository
from aiogram import F
from aiogram.types import *
from app.services.search_services.telegram_walker import TelegramWalker
from app.services.translater import t as transl
from aiogram.utils.formatting import *
from app.apps.core.bot.enum import SearchStatus, SearchType
from app.apps.core.repositories.search_repository import SearchRepository
from typing import List
from app.apps.core.models import Search
from app.services.search_services.telegram import TelegramSearchService

from app.apps.core.DTO import SearchTelegramAccount
from asgiref.sync import async_to_sync


searches: List[Search] = async_to_sync(SearchRepository.get)(status=SearchStatus.ready.name, search_type=SearchType.telegram_chats.name)

service = TelegramSearchService(searches)


# asyncio.run(service.handle())
asyncio.run(TelegramWalker().get_chat_info(chat_id=-1002079610546))

