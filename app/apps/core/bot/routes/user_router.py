from app.apps.core.bot.services.router import Router
import inspect
from aiogram.filters import Command
import aiogram.utils.formatting
from app.apps.core.bot.controllers.start import StartController as StartCommand
from app.apps.core.bot.controllers.user import UserController as UserCommands
from app.apps.core.bot.controllers.job import JobController as JobCommands
from app.apps.core.bot.helpers import answer, messager
from app.config.application import INSTALLED_APPS
from aiogram import F
import json
from typing import *
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BotCommand
from aiogram import Bot, types, F
from app.apps.core.bot.states import GetUsername, WorkState
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.apps.core.bot.keyboards.search import set_chats, set_keywords
from app.services.translater import t as transl
from aiogram.utils.formatting import *
from app.apps.core.bot.services.messager import Messager
from aiogram.utils.chat_action import ChatActionSender
from app.apps.core.bot.controllers._base_controller import BaseController
from app.apps.core.bot.controllers.search import SearchController
from app.apps.core.bot.controllers.advanced_mode import AdvancedModeController
from app.apps.core.bot.keyboards.main import allow_writer
from aiogram.filters import  Filter

router = Router()


router.action_message(StartCommand, StartCommand.__call__,
                      Command(commands=["start"]))

router.action_message(UserCommands, UserCommands.set_name,
                      GetUsername.get_username)

router.action_message(JobCommands, JobCommands.set_chat, F.chat_shared)


# TODO make action route 
# router.action(JobCommands, JobCommands.set_keywords, 'start_set_advanced_mode')
    
    
    

@router.message(F.text == 'Стать админом')
async def start_search(message: Message):
    await UserCommands(message).ask_writer()       

@router.message(F.text == 'Оставить отзыв')
async def start_search(message: Message):
    await UserCommands(message).send_review()    
    
    

@router.callback_query(UserCallbackData.filter(F.action == 'allow_writer'))
async def start_search(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: UserCallbackData
):
   await UserCommands(call.message, bot).allow_writer(callback_data)    



class WebAppDataFilter(Filter):
    async def __call__(self, message: Message, **kwargs) -> Union[bool, Dict[str, Any]]:
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False
# Хэндлер для обработки we_app_data
@router.message(WebAppDataFilter())
async def web_app_data(message: Message, state: FSMContext):
    data =  json.loads(message.web_app_data.data)
    print(data)