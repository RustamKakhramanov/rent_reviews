from aiogram.filters.callback_data import CallbackData
from app.apps.core.DTO import KeywordsDto


class UserCallbackData(CallbackData, prefix='user'):
    action: str
    type: str | None = None
    id: int | None = None
    name: str | None = None
    search_id: int | None = None
    tariff_id: int | None = None
    message_id: int | str | None = None
    keywords: dict | None = None


class AdvancedModeCallbackData(CallbackData, prefix='advanced_mode'):
    action: str
    type: str | None = None
    id: int | None = None
    message_id: int | str | None = None
    api_id: str | None = None
    api_hash: str | None = None
    sms_code: str | None = None


class SearchCallbackData(CallbackData, prefix='user'):
    action: str
    id: int | None = None
    search_id: int | None = None
    tariff_id: int | None = None
    chat_id: int | str | None = None
    message_id: int | str | None = None
    keyword_name: str | None = None
    keywords_options: str | list | None = None
