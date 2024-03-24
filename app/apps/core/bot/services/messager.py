from aiogram.types import *
from app.services.translater import t as transl
from aiogram.utils.formatting import *
from app.apps.core.DTO import KeywordsDto, TariffDto
from app.apps.core.models import TelegramUser


class Messager:

    @staticmethod
    def empty():
        return Text('')

    @staticmethod
    def limit_chats(chats: list):
        return as_list(
            Bold(transl('info.max_count_chats_reached')),
            Messager.get_chats_info(chats)
        )

    @staticmethod
    def action_exception(title='wrong.action', msg=None):
        return as_list(
            Bold("❌" + transl(title)),
            msg,
        )

    @staticmethod
    def get_keywords(kws: list):
        return as_list(
            Bold(transl('info.keywords_reached')),
            Messager.get_keywords_info(kws)
        )

    @staticmethod
    def q_reached():
        return Bold(transl('info.max_count_reached'))

    @staticmethod
    def get_keywords_info(dto: KeywordsDto):
        return as_list(
            Bold(transl('info.your_keywords') + ": "+dto.name),
            as_marked_list(
                marker='✅ ',
                *dto.options
            )
        )

    @staticmethod
    def limit_chats_set_words():
        return as_list(
            Bold(transl('info.max_count_chats_reached')),
            Messager.set_keywords()
        )

    @staticmethod
    def choise_action():
        return as_list(
            Bold(transl('buttons.choice_action'))
        )

    @staticmethod
    def set_keywords():
        return Bold(transl('actions.set_words'))

    @staticmethod
    def get_chats_info(chats: list):
        list = []

        for chat in chats:
            list += [f"id: {chat}"]

        return as_list(
            Bold(transl('info.your_chats') + f"({len(chats)}):"),
            as_list(
                as_list(
                    *list
                )
            )
        )

    @staticmethod
    def get_chats(chats: list, reached: None | Message = None):
        if (reached):
            return Messager.limit_chats(chats)

        return Messager.get_chats_info(chats)

  

    @staticmethod
    def get_search_status(status: str):
        return Bold(transl(f'info.search.status.{status}'))

    @staticmethod
    def about():
        return as_list(
            Bold(transl('get_started')),
        )
        
        
    @staticmethod
    def ask_writer(user: TelegramUser, allowed = None):
        args = (  as_key_value('Username', user.telegram_username),
                as_key_value('Имя', user.telegram_name),
                TextLink('Написать', url=f'https://t.me/{user.telegram_username}'))
        
        return as_list(
            Bold('Пользователь утвержден на права оставлять отзывы') if allowed  else  Bold('Пользователь запросил права на отзывы') ,
            as_list(
               *args
            )
        )

    @staticmethod
    def show_advanced_mode_info():
        return as_section(
            Bold(transl('info.telegram.advanced_mode.title')),
            as_line(as_key_value(
                transl('info.source'),
                TextLink('core.telegram.org/api/obtaining_api_id',
                         url='https://core.telegram.org/api/obtaining_api_id')
            )
            ),

            as_marked_list(
                Text(transl('info.telegram.advanced_mode.steps.signup')),
                Text(transl('info.telegram.advanced_mode.steps.api_tools')),
                # https://my.telegram.org/apps
                Text(transl('info.telegram.advanced_mode.steps.basic_adress')),
                Text(transl('info.telegram.advanced_mode.steps.only_api_id')),
            ),

        )

    @staticmethod
    def get_tariff_info(tariff: TariffDto):
        list = (
            (transl('info.tariff.chats_count', variables={
             'count': tariff.group_quantity})),
            (transl('info.tariff.keywords_count',
             variables={'count': tariff.keyword_quantity})),
            (transl('info.tariff.daemon_hours_quantity',
             variables={'count': tariff.daemon_hours_quantity})),
            (transl('info.tariff.week_searches', variables={
             'count': tariff.allowed_searches})),
        )

        return as_section(
            Bold(transl('info.tariff.name', variables={'name': tariff.name})),
            as_list(
                Underline('✅ '+transl('info.tariff.available') + ':'),
                as_marked_list(
                    *list
                )

            )
        )
