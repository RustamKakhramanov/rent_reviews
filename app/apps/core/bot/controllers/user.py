from aiogram import Router
from aiogram.filters import Command
from app.apps.core.bot.cases.telegram_user_case import TelegramUserCase
from app.config.application import INSTALLED_APPS
from aiogram import F
from asgiref.sync import sync_to_async
from typing import *
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BotCommand
from app.apps.core.bot.controllers._base_controller import BaseController
from aiogram import Bot, Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.translater import t as trans
from app.apps.core.bot.filters import UserCallbackData

class UserController(BaseController):
    case: TelegramUserCase = TelegramUserCase()
    
    async def set_name(self):
        await self.case.check_and_set_name()
        
        
    async def ask_writer(self):
        await self.case.ask_writer()    
            
    async def allow_writer(self, data:UserCallbackData):
        await self.case.allow_writer(data)  
        

