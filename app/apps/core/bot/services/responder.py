import aiogram
import asyncio
from aiogram.types import *

from app.services.translater import t as transl
from aiogram.utils.formatting import *
from aiogram.enums import *
from aiogram import Bot

# TODO Change for only bot manipulation


class Responder:
    message: Message

    def __init__(self, entity: Bot | Message):
        if isinstance(entity, Message):
            self.message = entity
            self.bot = entity.bot
        else:
            self.bot = entity

    def get_content(self, content):
        if isinstance(content, Text):
            return [content.as_html(), ParseMode.HTML]

        return [content, None]

    async def message_manipulate(self, content, method='answer', reply_markup=None, autodelete_seconds: int | None = None, **args):
        msg_text, parse_method = self.get_content(content)

        if method and hasattr(self.message, method) and callable(func := getattr(self.message, method)):
            message = await func(msg_text, reply_markup=reply_markup, can_be_edited=True, parse_mode=parse_method, **args)

        if autodelete_seconds:
            await self.delete_msg(message, autodelete_seconds)

        return message

    async def bot_manipulate(self,
                             content:Text|InputMedia|str,
                             chat_id: int|str|None = None,
                             reply_markup=None,
                             autodelete_seconds: int | None = None,
                             method='send_message',
                             bot: aiogram.Bot | None = None, **args
                             ):
        
        msg_text, parse_method = self.get_content(content)

        if not bot:
            bot = self.bot

        if method and hasattr(bot, method) and callable(func := getattr(bot, method)):
            message = await func(chat_id, msg_text, reply_markup=reply_markup,  parse_mode=parse_method, **args)

        if autodelete_seconds:
            await Responder.delete_msg(message, autodelete_seconds)

        return message

    async def edit(self, content: Text, reply_markup=None, autodelete_seconds: int | None = None, **args):
        return await self.message_manipulate(content=content, method='edit_text', reply_markup=reply_markup, autodelete_seconds=autodelete_seconds, **args)

    async def answer(self, content: Text | str, reply_markup=None, autodelete_seconds: int | None = None, **args):
        return await self.message_manipulate(content=content, reply_markup=reply_markup, autodelete_seconds=autodelete_seconds, **args)

    async def reply(self, content: Text | str, reply_markup=None, autodelete_seconds: int | None = None, **args) -> Message:
        return await self.message_manipulate(content=content, method='reply', reply_markup=reply_markup, autodelete_seconds=autodelete_seconds, **args)

    async def html_auto_deleted_reply(self, content: Text, reply_markup=None, seconds=3, *args):
        message = await self.message.reply(content.as_html(), reply_markup=reply_markup, parse_mode=ParseMode.HTML,  *args)
        self.delete_msg(message, seconds)

    async def delete_msg(self, message: Message | None = None, autodelete_seconds: int | None = None):
        if autodelete_seconds:
            await asyncio.sleep(autodelete_seconds)

        if not message:
            message = self.message

        return await self.force_delete(message.chat.id, message.message_id)

    async def force_delete(self, chat_id, msg_id):
        return await self.bot.delete_message(chat_id, msg_id)

    async def edit_reply_markup(self, markup, message_id: str | None = None, **args):
        return await self.message.edit_reply_markup(inline_message_id=message_id, reply_markup=markup,  **args)

    async def edit_chat_markup(self, markup, chat_id: str | None = None, **args):
        return

    async def delete_reply_markup(self, **args):
        return await self.message.delete_reply_markup(**args)
