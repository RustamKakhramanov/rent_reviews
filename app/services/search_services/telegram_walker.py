from app.apps.core.DTO import SearchTelegramAccount
from app.apps.core.repositories.search_telegram_user import SearchTelehramUserRepository

from telethon import utils, TelegramClient

from app.services.telethon_sessions import telegram_daemon, telegram_iteration
from telethon import functions, types
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.chatlists import JoinChatlistInviteRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel


class TelegramWalker:
        
    def __init__(self) -> None:
       pass
        
    
    async def parse_messages():
        pass
    
    async def subscribe_to_chat(self):
        pass 
    
    # @telegram_iteration()
    async def get_chat_info(self, client:TelegramClient, chat_id):
        return False
        result = await client(functions.channels.JoinChannelRequest(
            channel=chat_id
        ))
        print(result)
   
    # @telegram_iteration()
    async def is_can_parse_from_chat(self, chat_id) -> bool:
        return False
        result = await client(functions.channels.JoinChannelRequest(
            channel=chat_id
        ))
        print(result)

