from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.services.translater import t

class Tariff:
    actions: InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=t('buttons.tariff.change'),
                callback_data='tariff.change'
            ),
            InlineKeyboardButton(
                text=t('buttons.tariff.update'),
                callback_data='tariff.update'

            ),
        ]
    ])