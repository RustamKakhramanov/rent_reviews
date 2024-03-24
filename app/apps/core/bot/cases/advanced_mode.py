from typing import Final
from asgiref.sync import sync_to_async
from app.apps.core.models import TariffPlan, TelegramUser
from app.apps.core.bot.cases.__case import Case
from app.apps.core.repositories.user_repository import UserRepository
from app.apps.core.repositories.search_repository import SearchRepository
import aiogram.types
from app.apps.core.bot.states import GetUsername
from app.services.translater import t as transl
from aiogram.fsm.context import FSMContext
from app.apps.core.bot.filters import UserCallbackData
from app.services.redis import Redis
from aiogram.types import Message
from aiogram.utils.formatting import as_section, as_key_value, as_marked_section, Bold
from app.apps.core.bot.helpers import *
from app.apps.core.bot.keyboards.search import change_tariff


class AdvancedModeCase(Case):
    message: Message
    state: FSMContext

    @sync_to_async
    def change():

        return
