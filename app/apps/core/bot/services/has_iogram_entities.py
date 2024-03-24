from aiogram.types import *
from aiogram import *
from typing import Final
from asgiref.sync import sync_to_async
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class HasIogramEntites:
    message: Message
    state: FSMContext
    message: Message
    bot: Bot
    chat: Chat

    def set_message(self, message: Message):
        self.message = message

    def set_state(self, state: FSMContext):
        self.state = state

    def set_args(self, message: Message| None = None, bot: Bot | None = None, state: FSMContext | None = None) -> None:
        self.message = message
        self.chat = message.chat
        self.bot = bot
        self.state = state

    def __init__(self, message: Message, bot: Bot | None = None, state: FSMContext | None = None) -> None:
        self.set_args(message, bot, state)
        
        
    def get_user_id(self):
        return self.message.from_user.id  
          
    def get_msg_id(self):
        return self.message.message_id     
      
    def get_chat_id(self):
        return self.chat.id
