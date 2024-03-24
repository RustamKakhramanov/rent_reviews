from aiogram import Router
from aiogram.filters import Command
from app.apps.core.bot.cases.telegram_user_case import TelegramUserCase
from app.apps.core.bot.services.can_response import CanResponse
from app.config.application import INSTALLED_APPS
from aiogram import F
from typing import *
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BotCommand
from app.apps.core.repositories.user_repository import UserRepository
from aiogram import Bot, Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from app.apps.core.bot.cases.__case import Case
from app.apps.core.bot.services.has_iogram_entities import HasIogramEntites
from app.apps.core.bot.cases.work_case import WorkCase


class BaseController(HasIogramEntites, CanResponse):
    case: Case

    def __init__(self, *args):
        HasIogramEntites.__init__(self, *args)
        self.set_to_case()
        
        
    # def __init__(self, message: Message, bot: Bot | None = None, state: FSMContext | None = None):
    #     HasIogramEntites.__init__(self, message, bot, state)
    #     self.set_case()

    def set_to_case(self):
        if (self.case):
            self.case.set_args(
                self.message,
                self.bot,
                self.state
            )
