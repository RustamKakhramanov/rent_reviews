from app.apps.core.bot.controllers._base_controller import BaseController
from app.apps.core.bot.filters import UserCallbackData
from app.apps.core.bot.keyboards.buttons import make_inline_btn
from aiogram.utils.formatting import *
from app.apps.core.bot.cases.advanced_mode import AdvancedModeCase
from app.apps.core.bot.keyboards.advanced_mode import *
from app.apps.core.bot.helpers import messager
from app.apps.core.bot.keyboards.search import force_reply


class AdvancedModeController(BaseController):
    case: AdvancedModeCase = AdvancedModeCase()

    async def show_info(self, data: UserCallbackData):
        await self.message.delete()
        await self.response(
           messager('show_advanced_mode_info')
        )
        
        
       
        #  "info":{
        # "telegram":{
        #     "advanced_mode":{
        #         "steps":{
        #             "signup":"Зарегистрируйтесь в Telegram с помощью любого приложения.",
        #             "api_tools":"Перейти к разделу ‘API development tools’ и заполнить форму",
        #             "basic_adress":"Вы получите базовые адреса, а также параметры api_id и api_hash , необходимые для авторизации пользователя",
        #             "only_api_id":"На данный момент к любому номеру может быть привязан только один api_id"
        #         }
        #     }
        # },

    async def ask_token(self, data: UserCallbackData):
        await self.response('', force_reply())
    
    
    
    async def set_advanced_mode(data: UserCallbackData):
        pass
