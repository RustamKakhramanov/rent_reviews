from typing import Final
from asgiref.sync import sync_to_async
from app.apps.core.DTO import KeywordsDto, SearchDto
from app.apps.core.bot.enum import SearchStatus, SearchType
from app.apps.core.models import TariffPlan, TelegramUser
from app.apps.core.bot.cases.__case import Case
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.repositories.search_repository import SearchRepository
import aiogram.types
from app.apps.core.bot.states import GetUsername
from app.services.translater import t as transl
from aiogram.fsm.context import FSMContext
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.services.redis import Redis
from aiogram.types import Message
from aiogram.utils.formatting import as_section, as_key_value, as_marked_section, Bold
from app.apps.core.bot.helpers import *
from app.apps.core.bot.keyboards.search import change_tariff, search_status


class SearchCase(Case):
    async def make_search(self, user:TelegramUser, tariff:TariffPlan, callback_data: SearchCallbackData):
        keywords: KeywordsDto = SearchRepository.get_keywords_from_cache(callback_data.id, self.message.message_id)
        data: SearchDto = SearchRepository.get_search_from_cache(callback_data.id)

        data.set_attributes({
            'search_type': SearchType.telegram_chats.name,
            'entity_message_id': self.message.message_id,
            'entity_chat_id': self.message.chat.id,
            'status': SearchStatus.ready.name,
            'user': user,
            'keywords': keywords,
            'tariff': tariff
        })

        return await SearchRepository.store(data)
       
