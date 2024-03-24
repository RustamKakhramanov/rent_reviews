from typing import Final
from asgiref.sync import sync_to_async
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.apps.core.bot.services.responder import Responder
from app.apps.core.bot.services.can_response import CanResponse
from app.apps.core.bot.services.has_iogram_entities import HasIogramEntites


class Case(CanResponse, HasIogramEntites):
               
    def __init__(self, message: Message | None = None) -> None:
        if message:
            self.message = message
            

       