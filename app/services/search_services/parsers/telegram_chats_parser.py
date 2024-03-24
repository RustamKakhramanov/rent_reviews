

from app.apps.core.DTO import ChatsWithOrdersDto
from app.services.search_services.base import HasSearchEntities
from typing import *

# from app.services.telethon_sessions import telegram_iteration, telegram_daemon



class TelegramChatsParser(HasSearchEntities):
    
    
    async def scan_chats_and_parse_leads(self, chats_orders:List[ChatsWithOrdersDto]):
        result  = []
        
        for chat in chats_orders:
            pass
        
        
        return []