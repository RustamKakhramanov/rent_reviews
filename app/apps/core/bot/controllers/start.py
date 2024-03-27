from aiogram import Router
from aiogram.filters import Command
from app.apps.core.bot.cases.telegram_user_case import TelegramUserCase
from app.config.application import INSTALLED_APPS
from aiogram import F
from typing import *
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BotCommand
from app.apps.core.bot.controllers._base_controller import BaseController
from aiogram import Bot, Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.translater import t as trans
from app.apps.core.bot.states import WorkState


class StartController(BaseController):
    case: TelegramUserCase = TelegramUserCase()

    async def __call__(self):
        message = self.message
        if message.from_user is None:
            return
        
        await self.case.handle_start()
       
