

from abc import abstractmethod
from aiogram import Bot
import aiogram.exceptions
import asgiref.sync
from app.apps.core.repositories.search_telegram_user import SearchTelehramUserRepository
from app.services.search_services.base import BaseClient, HasSearchEntities
from telethon import TelegramClient
import telethon
from typing import *
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, types, F
from app.config.bot import RUNNING_MODE, TG_TOKEN, RunningMode
from app.apps.core.models import Search
from asgiref.sync import async_to_sync, sync_to_async
from app.services.error_logger import ErrorLogger
from app.apps.core.bot.services.responder import Responder
from typing import List
from aiogram.exceptions import *
from app.services.search_services.entites_maker import EntitiesMaker
from app.services.search_services.info.telegram_informator import TelegramInformator
from app.services.search_services.parsers.telegram_chats_parser import TelegramChatsParser
from app.apps.core.DTO import SearchTelegramAccount
from app.services.telethon_sessions import telegram_daemon, telegram_iteration

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetUsersRequest


class TelegramSearchService(HasSearchEntities):
    informator = TelegramInformator()
    chat_parser:TelegramChatsParser
 
    
    async def scan_chats_and_get_info(self):
       return  self.chat_parser.scan_chats_and_parse_leads()      
    
    def init_other_services(self):
        pass        
        
    def __init__(self, searches: List[Search]) -> None:
        self.set_attributes({'searches': searches})
     
 
        
     
        
    async def handle(self):
        chats_orders = EntitiesMaker.make_unique_chats_with_orders(self.searches)
        
        chats_with_leads = await TelegramChatsParser().scan_chats_and_parse_leads(chats_orders)
        
        
        
        
        
        # for chat in chats:
        #     await chats_parser.scan_chats_and_get_leads(client, chat)
        
        # history = await client(GetHistoryRequest(
        #         peer=-1002079817718,
        #         offset_id=3,
        #         offset_date=None, add_offset=0,
        #         limit=12, max_id=0, min_id=0,
        #         hash=0))
        
        # print(history)
    #    return await client.send_message('me', 'Hello, Shvabraide!') 