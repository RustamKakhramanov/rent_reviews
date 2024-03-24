from aiogram.utils.keyboard import *
from aiogram.types import *
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.services.translater import t as transl
from app.apps.core.DTO import KeywordsDto
from app.apps.core.bot.keyboards.buttons import *


def start_search(user_id, search_id=None) -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder().button(
        text=transl('buttons.bot.start_search'),
        callback_data=UserCallbackData(
            action='start_search', id=user_id, search_id=search_id).pack()
    ).as_markup(resize_keyboard=True)


def keywords_keyboard(user_id, dto: KeywordsDto, search_id=None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=transl('buttons.bot.start_search'),
        callback_data=SearchCallbackData(
            action='start_search',
            id=user_id,
            search_id=search_id,
            keyword_name=dto.name,
        ).pack()
    )

    builder.add(
        clear_btn(action='unset_keywords', id=user_id, search_id=search_id)
    )

    return builder.as_markup(resize_keyboard=True)


def change_tariff(user_id, tariff_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [

                change_tariff_btn(user_id, tariff_id)
            ]
        ], resize_keyboard=True)


def force_reply(placeholder: str | None = None):
    return ForceReply(input_field_placeholder=placeholder)


def clear_chats(user_id, tariff_id=None, show_save=True):
    builder = InlineKeyboardBuilder()
    builder.add(clear_chat_btn(user_id))

    if (tariff_id):
        builder.add(
            change_tariff_btn(id=user_id, tariff_id=tariff_id,
                              action_type='chats_reached')
        )

    if (show_save):
        builder.row(
            save_btn(action='save_chats', id=user_id, tariff_id=tariff_id)
        )

    return builder.as_markup(resize_keyboard=True)


def search_status(user_id, search_msg_id, chat_id, search_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=transl('buttons.status'),
                callback_data=SearchCallbackData(
                    action='search_status',
                    id=user_id,
                    chat_id=chat_id,
                    search_id=search_id,
                    message_id=search_msg_id
                ).pack()
            )
        ]
    ])
    
def search_status_or_delete(user_id, search_msg_id, chat_id, search_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            make_inline_btn(
                    transl_text='buttons.status',
                    action='search_status',
                    callback_data=SearchCallbackData,
                    id=user_id,
                    chat_id=chat_id,
                    search_id=search_id,
                    message_id=search_msg_id
                    
            ),  
                   
            make_inline_btn(
                    transl_text='buttons.delete',
                    action='delete_search',
                    callback_data=SearchCallbackData,
                    id=user_id,
                    chat_id=chat_id,
                    search_id=search_id,
                    message_id=search_msg_id
            )
        ]
    ])


def buy_tariff_inline(user_id, tariff_id=None, msg_id: Message = None, action_type='expired'):
    builder = InlineKeyboardBuilder()

    builder.add(
        change_tariff_btn(user_id, tariff_id, msg_id, action_type)
    )

    return builder.as_markup(resize_keyboard=True)

def ask_advanced_mode():
    builder = InlineKeyboardBuilder()

    builder.add(
        make_inline_btn(
                    transl_text='buttons.ask_advanced_mode',
                    action='advanced_mode_info',
            ), 
    )
    builder.add(
        delete_msg(btn_text='buttons.ignore')
    )

    return builder.as_markup(resize_keyboard=True)


def set_chats_keyboard(user_id, tariff_id=None, limit_msg: Message | None = None, show_save: bool =True):
    builder = InlineKeyboardBuilder()
    
    if (isinstance(limit_msg, Message)):
        limit_id = limit_msg.message_id
    else:
        limit_id = None
        
    builder.add(clear_chat_btn(id=user_id, msg_id=limit_id))
    
    if (tariff_id and limit_msg):
        builder.add(
            change_tariff_btn(user_id, tariff_id, limit_id, 'chats_reached')
        )

    if (not limit_msg and show_save):
        builder.add(
            save_btn(action='save_chats', id=user_id, tariff_id=tariff_id)
        )

    return builder.as_markup(resize_keyboard=True)


def next_step(step='set_chats'):
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(
                text=transl('buttons.bot.nex_step'),
                callback_data=step
                ))

    return builder.as_markup(resize_keyboard=True)


def set_chats(id, show=True, chat_id=None):
    builder = ReplyKeyboardBuilder()

    if (show):
        builder.add(request_chat_btn(id))

    return builder.as_markup(resize_keyboard=True)


def set_keywords(show=True):
    builder = ReplyKeyboardBuilder()

    if (show):
        builder.add(request_poll_btn())

    return builder.as_markup(resize_keyboard=True)


def max_chats(id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=transl('buttons.bot.nex_step'),
                    callback_data='for_keywords'
                ),
                KeyboardButton(
                    text=transl('buttons.bot.clear_chats'),
                    callback_data='clear_search_chats'
                ),
            ]
        ], resize_keyboard=True)
