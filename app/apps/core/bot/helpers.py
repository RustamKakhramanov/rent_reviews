from  aiogram.types import Message
from app.apps.core.bot.services.responder import Responder
from app.apps.core.bot.services.messager import Messager
from aiogram.utils.formatting import Text
import random


def messager( method:str = '', *args) -> Messager|Text:
    if method and hasattr(Messager, method) and callable(func := getattr(Messager, method)):
        return func(*args)
    return Messager

async def answer(m:Message, text, *args):
    return await Responder(m).answer(text, *args)


def get_chats_sending_id():
    return random.randint(3, 5)
   
    
    