from app.apps.core.bot.cases.telegram_user_case import TelegramUserCase
from app.apps.core.bot.cases.work_case import WorkCase
import json
import random
from typing import *
from aiogram.types import *
from app.apps.core.bot.controllers._base_controller import BaseController
from app.apps.core.bot.states import GetUsername, WorkState
from app.apps.core.bot.filters import UserCallbackData
from app.services.search_services.telegram_walker import TelegramWalker
from app.services.translater import t as trans
from aiogram import Bot, Router, types, F
from app.services.translater import t as transl
from app.services.redis import Redis
from app.apps.core.bot.keyboards.search import (clear_chats, next_step, set_chats,
    set_chats_keyboard, set_keywords)
from app.apps.core.repositories.search_repository import SearchRepository
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.bot.helpers import messager
from app.apps.core.repositories.tariff_repository import TariffRepository
from aiogram.enums import *


class JobController(BaseController):
    case: WorkCase = WorkCase()

    async def save_chats(self, callback_data:UserCallbackData):
        data = SearchRepository.get_search_from_cache(callback_data.id)
        tariff = await UserRepository.get_permited_tariff(callback_data.id)
        
        await self.edit(
            text=messager('get_chats', data.chats),
            reply_markup=set_chats_keyboard(
                callback_data.id, tariff.id, show_save=False)
        )
        
        return await self.response(messager('set_keywords'), reply_markup=set_keywords())
    
    async def set_chat(self):
        data = SearchRepository.get_search_from_cache(self.get_user_id())
        tariff = await UserRepository.get_permited_tariff(self.get_user_id())
        new_chat_id = self.message.chat_shared.chat_id
        
        if await TelegramWalker().is_can_parse_from_chat(chat_id=new_chat_id):
            return await self.case.set_chat(data, tariff, new_chat_id)
        else:
            return await self.case.cant_parse_private_chat(data, tariff)
         

    async def unset_chats(self, data: UserCallbackData):
        await self.case.unset_chats(data)
        

    async def unset_keywords(self, data: UserCallbackData):
        await self.case.unset_keywords(data)
       

    async def set_keywords(self):
       await self.case.set_keywords()
       await self.bot.delete_message(self.chat.id, self.message.message_id)
