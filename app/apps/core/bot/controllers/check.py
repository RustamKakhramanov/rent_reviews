from aiogram import Router
import aiogram.enums
from aiogram.filters import Command
from app.apps.core.DTO import DebtorSearchState
from app.apps.core.bot.cases.telegram_user_case import TelegramUserCase
from app.config.application import INSTALLED_APPS
from aiogram import F
from asgiref.sync import sync_to_async
from typing import *
import aiogram.types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BotCommand
from app.apps.core.bot.controllers._base_controller import BaseController
from aiogram import Bot, Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.translater import t as trans
from app.apps.core.bot.filters import UserCallbackData
from app.apps.core.bot.helpers import get_debtor_info
from aiogram.utils.formatting import *
from app.apps.core.repositories.debtor_repository import DebtorRepository
from app.apps.core.bot.enum import ReviewStatus
from aiogram.types import *
from app.apps.core.bot.keyboards.main import moderate_review
from aiogram.enums import ParseMode
import datetime

class CheckController(BaseController):
    case: TelegramUserCase = TelegramUserCase()
    repo: DebtorRepository = DebtorRepository
    message: Message
    state: FSMContext

    def get_years_from_iin(self, iin: str) -> List[int]:
        today = datetime.date.today()
    
        year_str = iin[:2]
        if (year_str[0] == '0'):
            year = int(f'20{year_str}')
        else:
            year = int(f'19{year_str}')
        
        month = int(iin[2:4])
        day = int(iin[4:6])
        
        born = datetime.datetime.strptime(f'{day}.{month}.{year}', '%d.%m.%Y' )
        
        age =   today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        
        return [age,f'{day}.{month}.{year}' ]
    
    
    async def check_iin(self,   state: FSMContext):
        # iin = "960820351854"
        iin = self.message.text

        if iin and iin.isnumeric() and len(iin) == 12:
            from_api_info = get_debtor_info(iin)
            from_db = await self.repo.get_by_iin(iin=iin)
            if (from_db or from_api_info):
                for deb in from_db:
                    info = as_section(
                        f"Информация из базы данных по иин: {iin}",
                        as_list(
                            as_key_value(
                                'Должник',  f"{deb.firstname} {deb.lastname}"),
                            as_key_value('Обстоятельства', deb.text),
                        ))
                    await self.message.answer(info.as_html())

            if (from_api_info):
                for item in from_api_info:
                    info = as_list(
                        as_key_value(
                            'Орган, выдавший исполнительный документ', item['ilOrganRu']),
                        as_key_value(
                            'Номер исполнительного производства и дата возбуждения', item['ilDate']),
                        as_key_value(
                            'Должник',  f"{item['firstname']} {item['lastname']}"),
                        as_key_value('Взыскатель', item['recoverer']),
                        as_key_value('Сумма взысканий',
                                     item['recovery_amount']),
                        as_key_value('Орган исполнительного пр-ва',
                                     item['bailiffs']),
                    )

                    await self.message.answer(info.as_html())
            else:
                await self.response(
                    as_list(
                        as_section(
                        '',
                            as_list(
                                   as_key_value('ИИН', iin),
                                    as_key_value('Дата рождения',self.get_years_from_iin(iin)[0]),
                                    as_key_value('Возраст, лет', self.get_years_from_iin(iin)[1]),
                            )
                        ),
                        as_line(),
                        as_section(
                        '[Налоги]',
                            as_marked_list(
                                as_key_value(' ⁠Задолженности: ','Нет'),
                                marker='•⁠ '
                            )
                        ),
                        as_line(),
                        
                        as_section(
                        '[Сведения о предстоящих платежах]',
                            as_marked_list(
                                as_key_value(' ⁠Предстоящие платежи с учетом переплаты','0 тг'),
                                marker='•⁠ '
                            )
                        ),
                        as_line(),
                        
                        as_section(
                        '[Реестр должников]',
                            as_marked_list(
                                as_key_value('⁠Задолженности','Нет'),
                                marker='•⁠ '
                            )
                        ),
                        as_line(),
                        
                        as_section(
                        '[Ограничение на выезд из РК]',
                            as_marked_list(
                                as_key_value('⁠Выезд запрещен','Нет'),
                                marker='•⁠ '
                            )
                        ),
                        as_line(),
                        
                        as_section(
                        '[Аресты]',
                            as_marked_list(
                                as_key_value('⁠Арест на банковские счета','Нет'),
                                as_key_value('⁠Временное ограничение на выезд из РК','Нет'),
                                as_key_value('⁠Запрет на регистрационные действия','Нет'),
                                as_key_value('⁠Запрет на совершение нотариальных действий','Нет'),
                                as_key_value('⁠Арест на имущество','Нет'),
                                as_key_value('Арест на транспорт','Нет'),
                                marker='•⁠ '
                            )
                        ),
                          as_line(),
                        as_section(
                        '[Прокаты, аренда]',
                            as_marked_list(
                                as_key_value('Информация по прокатам','Не найдено'),
                                marker='•⁠ '
                            )
                        ),
                    )
                        )
        else:
            await state.set_state(DebtorSearchState.iin)
            await self.response('ИИН должен быть 12 символьным числом, введите заново', autodelete_seconds=3)

    async def allow_review(self, data: UserCallbackData):
        result = await self.repo.update_and_find(data.id, status=ReviewStatus.APPROVED.value)

        if (result):
            msg = as_section('Отзыв утвержден', as_list(
                as_key_value('ИИН', result.iin_or_bin),
                as_key_value('Имя', result.firstname),
                as_key_value('Фамилия', result.lastname),
                as_key_value('Текст', result.text),
            )).as_html()

            if result.user:
                await self.message.bot.send_message(result.user.telegram_id, msg)

            await self.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text='Удалить',
                    callback_data=UserCallbackData(action='delete_review', id=result.id).pack()),
            ]]))

    async def edit_review(self, state: FSMContext):
        data = await state.get_data()
        if 'review_id' in data:
            review_id = data['review_id']
            result = await self.repo.update_and_find(review_id, text=self.message.text)
            if result:
                msg = as_section('Отзыв отредактирован', as_list(
                    as_key_value(
                        f'Отправивший отзыв:', f' {result.user.telegram_username} {result.user.telegram_name}'),
                    as_key_value('ИИН', result.iin_or_bin),
                    as_key_value('Имя', result.firstname),
                    as_key_value('Фамилия', result.lastname),
                    as_key_value('Текст', result.text),
                ))

                await self.response(msg, reply_markup=moderate_review(result.id))

    async def delete_review(self, data: UserCallbackData):
        result = await self.repo.find(data.id)
        await self.repo.delete(data.id)

        msg = as_section('Отзыв был удален', as_list(
            as_key_value('ИИН', result.iin_or_bin),
            as_key_value('Имя', result.firstname),
            as_key_value('Фамилия', result.lastname),
            as_key_value('Текст', result.text),
        )).as_html()

        await self.message.edit_text(msg, reply_markup=None)

        if result.user:
            await self.message.bot.send_message(result.user.telegram_id,msg)
