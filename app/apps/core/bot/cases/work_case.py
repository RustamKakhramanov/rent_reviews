from aiogram.utils.formatting import Bold
import random
from typing import Final
from asgiref.sync import sync_to_async
from app.apps.core.models import TelegramUser
from app.apps.core.bot.cases.__case import Case
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.repositories.search_repository import SearchRepository
from app.services.translater import t as transl
from app.apps.core.bot.filters import UserCallbackData
from app.apps.core.bot.keyboards.search import *
from app.apps.core.bot.helpers import get_chats_sending_id, messager
from aiogram.types import *
from app.apps.core.DTO import KeywordsDto, SearchDto, TariffDto
from app.apps.core.repositories.tariff_repository import TariffRepository


class WorkCase(Case):
    async def set_keywords(self):
        data = SearchRepository.get_search_from_cache(self.get_user_id())
        tariff = await UserRepository.get_permited_tariff(self.get_user_id())
        allowed = tariff.keyword_quantity
        keywords = self.parse_keywords(self.message.poll.options, allowed)

        dto = KeywordsDto({
            'name': self.message.poll.question,
            'options': keywords
        })

        if len(data.chats) == 0:
            return await self.resolve_get_chats_message(data, tariff)

        if allowed:
            message = await self.response(
                text=messager('get_keywords_info', dto),
                reply_markup=keywords_keyboard(
                    self.get_user_id(), dto)
            )

            SearchRepository.set_keywords_to_cache(
                self.get_user_id(), message.message_id, dto.to_dict())
        else:
            await self.action_exception(
                text=Bold(transl('wrong.tariff_limit')),
                reply_markup=buy_tariff_inline(
                    self.get_user_id(),
                    tariff_id=tariff.id,
                    msg_id=self.get_msg_id(),
                    action_type='keywords_expired'
                )
            )

    async def unset_keywords(self, callback_data: UserCallbackData):
        SearchRepository.remove_keywords_from_cache(
            callback_data.id, callback_data.message_id)
        return await self.message.delete()

    async def cant_parse_private_chat(self, data: SearchDto, tariff: TariffDto):
        await self.action_exception(
            tilte='wrong.chat.unprivate',
            text=transl('info.search.cant_parse_private'),
            reply_markup=ask_advanced_mode()
        )
        if data.chats:
            await self.resolve_get_chats_message(data, tariff, about_limit=None)

    async def set_chat(self, data: SearchDto, tariff: TariffDto, chat_id):
        allowed_count = tariff.group_quantity

        if (not data):
            data = SearchRepository.get_initial_search()

        if chat_id not in data.chats and len(data.chats) < allowed_count:
            data.chats = data.chats + [chat_id]
            SearchRepository.set_to_cache(self.get_user_id(), data)

        if (len(data.chats) >= allowed_count):
            about_limit = await self.reply(messager('limit_chats_set_words'), reply_markup=set_keywords())
        else:
            about_limit = None

        await self.resolve_get_chats_message(data, tariff, about_limit)

    async def unset_chats(self, callback_data: UserCallbackData):
        data = SearchRepository.get_search_from_cache(callback_data.id)

        if data:
            data.chats = []
            SearchRepository.set_to_cache(callback_data.id, data)

        if callback_data.message_id:
            await self.force_delete_msg(self.chat.id, callback_data.message_id)

        message = await self.edit(
            transl('info.chats_cleared'),
            reply_markup=None,
        )

        await self.response(
            transl('actions.set_chats'),
            reply_markup=set_chats(get_chats_sending_id(), True),
        )

        await self.delete_message(message, autodelete_seconds=1)

    def parse_keywords(s, kws, allowed=None):
        parsed_kws = []

        for kw in kws:
            parsed_kws.append(kw.text)

        return parsed_kws
