from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Router as IoRouter, types, F
from app.apps.core.bot.services.has_iogram_entities import HasIogramEntites
from typing import *
from aiogram.dispatcher.event.handler import CallbackType
from app.apps.core.bot.filters import UserCallbackData


class Caller:
    controller_name = None
    action = None
    method_args = None
    type = None

     
    def load(self, type, c_name, action, *filters: CallbackType, m_args: dict = {}):
        self.type = type
        self.controller_name = c_name
        self.action = action.__name__
        self.method_args = m_args
        return self

    def get_call(self):
        RESOLVERS = {
            'message': self.resolve_message
        }

        if self.type in RESOLVERS:
            return RESOLVERS[self.type]

    async def resolve_message(self, message: Message, bot: Bot | None = None, state: FSMContext | None = None):
        controller = self.controller_name(message, bot, state)

        if hasattr(self.controller_name, self.action) and callable(func := getattr(controller, self.action)):
            return await func(*self.method_args)
        
        
        
        
        


class Router(IoRouter):
    iogram_router = IoRouter()

    def register_callback(self, type, c_name, action, *filters: CallbackType, m_args: dict = {}):
        call = Caller().load(
            'message',
            c_name,
            action,
            *filters,
            m_args=m_args
        ).get_call()

     

        self.__dict__[type].register(call, *filters)

    def action_message(self, c_name, fn_name, *filters: CallbackType, a_args: dict = {}):
        self.register_callback('message', c_name, fn_name,
                               *filters, m_args=a_args)
        
    # def action(self, c_name, fn_name, action, callback_data=UserCallbackData, a_args: dict = {}):
    #     self.register_callback('message', c_name, action, m_args=a_args)
        
    def callback(self, c_name, action, *filters: CallbackType, a_args: dict = {}):
        self.register_callback('callback_query', c_name, action,
                               *filters, m_args=a_args)
