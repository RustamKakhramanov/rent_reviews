from aiogram.utils.keyboard import *
from aiogram.types import *
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.services.translater import t as transl
from app.apps.core.DTO import KeywordsDto
from app.apps.core.bot.keyboards.buttons import *


def advanced_info() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        make_inline_btn('buttons.continue', action='start_set_advanced_mode')
        
    )

    return builder.as_markup(resize_keyboard=True)



def set_token() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        make_inline_btn('buttons.continue', action='start_set_advanced_mode')
        
    )

    return builder.as_markup(resize_keyboard=True)