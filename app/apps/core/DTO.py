from typing import List
from django.db.models import Model
import json
from app.apps.core.models import Search, TariffPlan, TelegramUser
from app.apps.core.bot.enum import SearchType
from app.services.has_attributes import HasAttributes


class DTO(HasAttributes):
    def __init__(self, data: dict | Model| None):
        if isinstance(data, Model):
            data = data.__dict__

        if(data):
            self.set_attributes(data)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        dict = self.__dict__
        
        for key, item in dict.items():
            if isinstance(item, DTO):
                dict[key] = item.to_dict()
                
            elif isinstance(item, Model):
                dict[key] = item.__dict__
                
        return dict

    


class TariffDto(DTO):
    id: int | str = None
    name = None
    group_quantity = 0
    keyword_quantity = 0
    daemon_hours_quantity = 0
    allowed_searches = 0
    is_expired = 0


class KeywordsDto(DTO):
    name: str = None
    options: list = []


class SearchDto(DTO):
    id: int | str | None = None
    entity_message_id: str | int | None = None
    entity_chat_id: str | int | None = None
    entity_search_id: str | int | None = None
    status: str = 'initial'
    user: TelegramUser | None = None
    keywords: KeywordsDto | None = None
    chats: List[str] = []
    tariff_plan: TariffPlan|TariffDto  = None
    search_type: str|None = None

class TelegramInfoDto(DTO):
    content = None
    chat_id: str | int | None = None
    msg_id: str | int | None = None
    
    @staticmethod
    def multiparse(searches: List[Search], text):
        return [
                TelegramInfoDto({
                    'content': text,
                    'chat_id': search.entity_chat_id,
                    'msg_id': search.entity_message_id
                }) for search in searches
            ]
        
class  HandledSearch(DTO):
    content = None
    chat_id: str | int | None = None
    msg_id: str | int | None = None
    
    @staticmethod
    def multiparse(searches: List[Search], text):
        return [
                HandledSearch({
                    'content': text,
                    'chat_id': search.entity_chat_id,
                    'msg_id': search.entity_message_id
                }) for search in searches
            ]
        
        

class  SearchTelegramAccount(DTO):
    username:str = None
    password:str = None
    phone:str = None
    api_id = None
    api_hash = None
    bot_token = None
    
    
    

class SearchLead(DTO):
    name:str = None
    keywords=List[str]
    
    
class SearchOrderDTO(DTO):
    keywords: List[str] = None
    leads: List[SearchLead] = None
    user: TelegramUser | None = None

class ChatsWithOrdersDto(DTO):
    chat_id:str|int = None
    orders:List[SearchOrderDTO] = None