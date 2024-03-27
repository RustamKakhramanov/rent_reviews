from app.apps.core.DTO import DebtorSearchState, DebtorState
from app.apps.core.bot.services.router import Router
from aiogram.filters import Command
from app.apps.core.bot.controllers.start import StartController as StartCommand
from app.apps.core.bot.controllers.user import UserController as UserCommands
from app.apps.core.bot.controllers.job import JobController as JobCommands
from app.apps.core.bot.helpers import answer, messager
from app.apps.core.repositories.debtor_repository import DebtorRepository
from app.config.application import INSTALLED_APPS
from aiogram import F
import json
from typing import *
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand
from aiogram import Bot, types, F
from app.apps.core.bot.states import GetUsername, WorkState
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.apps.core.bot.keyboards.search import force_reply, set_chats, set_keywords
from app.services.translater import t as transl
from aiogram.utils.formatting import *
from aiogram.filters import  Filter
from app.apps.core.bot.controllers.check import CheckController
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.bot.keyboards.main import moderate_review
from aiogram.enums import ParseMode
from app.apps.core.bot.enum import ReviewStatus, UserRole
from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from app.apps.core.bot.keyboards.buttons import delete_msg

router = Router()

router.action_message(StartCommand, StartCommand.__call__,
                      Command(commands=["start"]))

router.action_message(UserCommands, UserCommands.set_name,
                      GetUsername.get_username)

router.action_message(JobCommands, JobCommands.set_chat, F.chat_shared)

class WebAppDataFilter(Filter):
    async def __call__(self, message: Message, **kwargs) -> Union[bool, Dict[str, Any]]:
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False
    
# Хэндлер для обработки we_app_data
@router.message(WebAppDataFilter())
async def web_app_data(message: Message, state: FSMContext):
    data =  json.loads(message.web_app_data.data)
    user = await UserRepository.find(id=message.from_user.id)
    data['user'] = user
    
    if(user.role==UserRole.ADMIN.value):
        data['status'] = ReviewStatus.ALLOWED
        
    debtor = await DebtorRepository.create(data)
    
    if(user.role==UserRole.ADMIN.value):
        await message.answer('Отзыв отправлен')
    else: 
        msg = as_section('Отзыв отправлен на модерацию и рассмотрение', as_list(
            as_key_value('Отправивший отзыв', f'{user.telegram_username}{user.telegram_name}'),
            as_key_value('ИИН', data['iin']),
            as_key_value('Имя', data['firstname']),
            as_key_value('Фамилия', data['lastname']),
            as_key_value('Текст', data['review_text']),
        )).as_html()
    
        for admin in await UserRepository.get_admins():
            await message.bot.send_message(chat_id=admin.telegram_id, text=msg, parse_mode=ParseMode.HTML, reply_markup=moderate_review(debtor.id))
        
        
        await message.answer('Отзыв отправлен на модерацию и рассмотрение')
    
    



@router.message(Command(commands=["search"]))
async def ask_check_iin(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(DebtorSearchState.iin)
    await message.answer("Введите иин")


@router.message(F.text == 'Добавить недобросовестного клиента')
async def start_search(message: Message):
    await UserCommands(message).ask_writer()  
 
      

@router.message(F.text == 'Проверить')
async def ask_check_iin(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(DebtorSearchState.iin)
    await message.answer("Введите иин")
   

@router.message(DebtorSearchState.iin)
async def check_iin(message: Message, state: FSMContext) -> None:
    await CheckController(message).check_iin(state)  
    

@router.callback_query(UserCallbackData.filter(F.action == 'allow_writer'))
async def start_search(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: UserCallbackData
):
   await UserCommands(call.message, bot).allow_writer(callback_data)      
   

@router.callback_query(UserCallbackData.filter(F.action == 'allow_review'))
async def allow_review(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: UserCallbackData
):
   await CheckController(call.message, bot).allow_review(callback_data)  
   
@router.callback_query(UserCallbackData.filter(F.action == 'ask_edit_review'))
async def ask_edit_review(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: UserCallbackData,
    state: FSMContext
):
    await state.update_data(review_id=callback_data.id)
    await state.set_state(DebtorState.text)
    await call.message.delete()
    await call.message.answer("Введите текст отзыва")
    
    
@router.message(DebtorState.text)
async def edit_review(message: Message, state: FSMContext) -> None:

        await CheckController(message).edit_review(state)  
    
    
@router.callback_query(UserCallbackData.filter(F.action == 'edit_review'))
async def edit_review(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: UserCallbackData
):
   await CheckController(call.message, bot).edit_review(callback_data)     

@router.callback_query(UserCallbackData.filter(F.action == 'delete_review'))
async def delete_review(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: UserCallbackData
):
   await CheckController(call.message, bot).delete_review(callback_data)    






