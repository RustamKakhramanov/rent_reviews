from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.services.translater import t

class Rules:
    initial = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=t('buttons.allowed_rules')
            )
        ]
    ])