

from abc import abstractmethod
from aiogram import Bot
from app.services.search_services.base import BaseClient
from typing import *
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, types, F
from app.config.bot import RUNNING_MODE, TG_TOKEN, RunningMode
from app.apps.core.models import Search
from asgiref.sync import async_to_sync, sync_to_async
from app.apps.core.DTO import TelegramInfoDto as InfoDto
from app.services.error_logger import ErrorLogger
from app.apps.core.bot.services.responder import Responder
from typing import List
from aiogram.exceptions import *



class TelegramInformator(BaseClient):
    bot: Bot

    def __init__(self) -> None:
        session = AiohttpSession()
        self.bot = Bot(token=TG_TOKEN, session=session)

    async def close_connection(self):
        await self.bot.session.close()

    async def info(self, searches: List[Search] | List[InfoDto], text: str | None):
        if not searches or len(searches) < 1:
            # TODO Error Logging
            ErrorLogger.log()
            return False

        if isinstance(searches[0],  Search) and not text:
            # TODO Error Logging
            ErrorLogger.log()
            return False

        if isinstance(searches[0], Search):
            dtos =  InfoDto.multiparse(searches, text)

        await self.send_msg(dtos)

    async def send_msg(self, informed: InfoDto | List[InfoDto]):
        async def send_or_reply_if_exists(dto: InfoDto):
            try:
                await Responder(self.bot).bot_manipulate(dto.content, dto.chat_id, reply_to_message_id=dto.msg_id)
            except TelegramBadRequest:
                await Responder(self.bot).bot_manipulate(dto.content, dto.chat_id, reply_to_message_id=None)
            finally:
                return False

        if isinstance(informed,  list):
            for item in informed:
                await send_or_reply_if_exists(item)

        else:
            await send_or_reply_if_exists(informed)

        await self.bot.session.close()

    def get_requester(self):
        return self.bot