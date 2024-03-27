from aiogram.utils.keyboard import *
from aiogram.types import *
from app.apps.core.bot.filters import SearchCallbackData, UserCallbackData
from app.apps.core.models import TelegramUser
from app.services.translater import t as transl
from app.apps.core.DTO import KeywordsDto
from app.apps.core.bot.keyboards.buttons import *
from app.apps.core.bot.enum import UserRole


def reply_keyboard(user: TelegramUser, hide_stay_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    if not hide_stay_admin:
        if user.role == UserRole.USER.value:
            builder.button( text='Добавить недобросовестного клиента')

    if user.role == UserRole.ADMIN.value or user.role == UserRole.WRITER.value:
        builder.button(text='Добавить недобросовестного клиента',  web_app=WebAppInfo(url="https://rent-reviews.vercel.app"))

    builder.button(text='Проверить')

    return builder.adjust(1,1).as_markup(resize_keyboard=False)


def allow_writer(user: TelegramUser) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard= [[
        InlineKeyboardButton(
            text='Утвердить',
            callback_data=UserCallbackData(action='allow_writer', id=user.telegram_id).pack())
    ]])

def moderate_review(review_id: TelegramUser) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard= [[
        InlineKeyboardButton(
            text='Утвердить',
            callback_data=UserCallbackData(action='allow_review', id=review_id).pack()),
        InlineKeyboardButton(
            text='Редактировать',
            callback_data=UserCallbackData(action='ask_edit_review', id=review_id).pack()),
        InlineKeyboardButton(
            text='Удалить',
            callback_data=UserCallbackData(action='delete_review', id=review_id).pack()),
    ]])


def start_keyboard(user: TelegramUser) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not user.is_admin:
        builder.button(
            text='Добавить недобросовестного клиента',
            callback_data=UserCallbackData(
                action='stay_admin',
                id=user.telegram_id,
            ).pack()
        )
    else:
        builder.button(
            text='Оставить отзыв',
            callback_data=UserCallbackData(
                action='send_review',
                id=user.telegram_id,
            ).pack()
        )

    builder.button(
        text='Проверить',
        callback_data=UserCallbackData(
            action='check_user',
            id=user.telegram_id
        ).pack()
    )

    return builder.adjust(1, 2).as_markup(resize_keyboard=False)
