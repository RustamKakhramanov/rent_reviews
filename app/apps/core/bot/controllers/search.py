from app.apps.core.bot.cases.telegram_user_case import TelegramUserCase
from app.apps.core.bot.cases.work_case import WorkCase
from app.apps.core.models import Search, TelegramUser
import asyncio
import random
from typing import *
from aiogram.types import *
from app.apps.core.bot.controllers._base_controller import BaseController
from app.apps.core.bot.states import GetUsername, WorkState
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.apps.core.repositories.search_repository import SearchRepository
from app.services.translater import t as trans
from aiogram import Bot, Router, types, F
from app.services.translater import t as transl
from app.services.redis import Redis
from app.apps.core.bot.keyboards.search import (buy_tariff_inline, clear_chats, next_step,
                                                search_status, search_status_or_delete, set_chats)
from app.apps.core.bot.cases.search import SearchCase
from app.apps.core.bot.helpers import messager
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.DTO import KeywordsDto, SearchDto, TariffDto
from app.apps.core.bot.enum import SearchStatus, SearchType
from app.apps.core.bot.services.responder import Responder
from aiogram.utils.formatting import *
from aiogram.enums import *

class SearchController(BaseController):
    case: SearchCase = SearchCase()

    async def get_status(self, callback_data: SearchCallbackData):
        search = SearchDto(
            await SearchRepository.find(callback_data.search_id)
        )

        if search.status == SearchStatus.ready.name or search.status == SearchStatus.in_process.name:
            status = SearchStatus.in_process.name
            return await self.reply(messager('get_search_status', status), autodelete_seconds=3)

        if search.status == SearchStatus.error.name:
            # TODO ERROR MESSAGE
            return

        if search.status == SearchStatus.finished.name:
            # TODO edit message with table
            return

    async def store(self, callback_data: SearchCallbackData):
        user: TelegramUser = await UserRepository.find(callback_data.id)
        tariff = await UserRepository.get_permited_tariff(user, with_dto=False)

        if tariff.keyword_quantity:
            search:Search = await self.case.make_search(user, tariff, callback_data)
            await self.edit(
                text=messager('get_search_info', search),
                reply_markup=search_status_or_delete(
                    self.get_user_id(),
                    self.get_msg_id(),
                    self.get_chat_id(),
                    search.id
                ))
        else:
            await self.reply(
                text=messager('q_reached'),
                reply_markup=buy_tariff_inline(
                    callback_data.id, tariff.id, self.get_msg_id(), action_type='keywords_reached')
            )
            
            
    async def delete(self, callback_data: SearchCallbackData):
        is_deleted = await SearchRepository.delete_if_alowed(callback_data.search_id)
        
        if is_deleted:
            await self.message.delete()
            return await self.response(transl('info.search.deleted'), autodelete_seconds=3)
        else:
            return self.action_exception(transl('info.try_again'))
