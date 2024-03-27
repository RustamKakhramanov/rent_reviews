import app.apps.core.bot.helpers
from app.apps.core.bot.services.messager import Messager
from typing import Final
from asgiref.sync import sync_to_async
from app.apps.core.models import TelegramUser
from app.apps.core.bot.cases.__case import Case
from app.apps.core.repositories.user_repository import UserRepository
from aiogram.types import Message
from app.apps.core.bot.states import GetUsername, WorkState
from app.services.translater import t as transl
from aiogram.fsm.context import FSMContext
from app.apps.core.bot.keyboards.search import change_tariff, force_reply, set_chats
from app.apps.core.repositories.search_repository import SearchRepository
import random
from app.apps.core.bot.cases.tariff_case import TariffCase
from app.apps.core.bot.helpers import answer
from app.apps.core.bot.keyboards.main import allow_writer, reply_keyboard, start_keyboard
from aiogram.utils.formatting import *
from app.apps.core.bot.filters import UserCallbackData
from app.apps.core.bot.enum import UserRole
from aiogram.enums import ParseMode


class TelegramUserCase(Case):
    repo: UserRepository = UserRepository
    message: Message
    state: FSMContext

    async def answer_for_name(self):
        await self.message.answer(transl('start.question_name'), reply_markup=force_reply())
        await self.state.set_state(GetUsername.get_username)

    async def answer_for_work(self, user: TelegramUser):
        text = as_list(
            Bold(f'Здравствуйте, {user.telegram_name}!'),
            'Начните работу с ботом. '
        )

        await self.response(text=text, reply_markup=reply_keyboard(user))
        
      

    async def handle_start(self):
        user = await self.findUser()

        if not user:
            user = await self.register_and_send_tariff_message()

        if not user.telegram_name:
            return await self.answer_for_name()

        await self.answer_for_work(user)

    async def check_and_set_name(self):
        message = self.message
        repo = self.repo

        if (repo.check_username(message.text) and await repo.exists(message.from_user.id)):
            user = await repo.fin_and_update(id=message.from_user.id,  telegram_name=message.text)
            await self.answer_for_work(user)
            await self.state.clear()
        else:
            await message.answer('wrong.name')

    # check Registration
    async def findUser(self) -> TelegramUser | None:
        return await self.repo.find(id=self.getUserObject('telegram_id'))

    # Registration
    async def register_and_send_tariff_message(
        self,
        message: None | Message = None,
    ) -> tuple[TelegramUser, bool]:
        user, tariff = await self.repo.save_and_set_tariff(data=self.getUserObject(), get_entities=True)

        return user

    # get User Object from Message
    def getUserObject(self, property: str | None = None):
        t_name = ''
        t_username = ''

        if (self.message.from_user.username):
            t_username += self.message.from_user.username

        if (self.message.from_user.first_name):
            t_name += self.message.from_user.first_name

        if (self.message.from_user.last_name):
            t_name += ' '+self.message.from_user.last_name

        data = {
            'telegram_id': self.message.from_user.id,
            'telegram_username': t_username,
            'telegram_name': t_name
        }

        if (property):
            return data[property]

        return data

    async def ask_writer(self):
        admins = await self.repo.get_admins()
        user = await self.repo.find(id=self.message.from_user.id)

        message = Messager.ask_writer(user)

        # if user and user.role == UserRole.USER.value:
        for admin in admins:
            await self.message.bot.send_message(chat_id=admin.telegram_id, text=message.as_html(), parse_mode=ParseMode.HTML, reply_markup=allow_writer(user))

        await self.repo.update(id=user.telegram_id, role=UserRole.REQUEST_WRITER.value)
        await self.message.answer('Ваш запрос принят на рассмотрение!', reply_markup=reply_keyboard(user, True))
        await self.message.delete()

    async def allow_writer(self, data: UserCallbackData):
        await self.repo.update(id=data.id, role=UserRole.WRITER.value)

        user = await self.repo.find(data.id)

        await self.bot.send_message(data.id, 'Ваш запрос одобрен!', reply_markup=reply_keyboard(user, True))
        await self.message.edit_text(Messager.ask_writer(user, True).as_html(), parse_mode=ParseMode.HTML, reply_markup=None)

    async def check_debtor(self):
        pass


CORE_USE_CASE: Final[TelegramUserCase] = TelegramUserCase()
