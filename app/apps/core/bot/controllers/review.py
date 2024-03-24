from aiogram import Router
from aiogram.filters import Command
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

class ReviewController(BaseController):
    def register_admin(self):
        pass
    
    def approve_user(self):
        pass
    
 

