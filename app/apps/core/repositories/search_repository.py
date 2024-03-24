import aiogram.types
import typing
from asgiref.sync import sync_to_async
from app.apps.core.models import Search, TelegramUser
from app.services.redis import Redis
from app.apps.core.DTO import KeywordsDto, SearchDto
from app.apps.core.bot.enum import SearchStatus
from app.apps.core.repositories.base import BaseRepository
import random

class SearchRepository(BaseRepository):
    @sync_to_async
    def save(self: None, data: SearchDto) -> Search:
        return Search.objects.get_or_create(
            telegram_id=data['telegram_id'],
            telegram_username=data['telegram_username'],
            telegram_name=data['telegram_name'],
        )

    @sync_to_async
    def store(self: None, data: SearchDto) -> Search:
        return Search.objects.create(
            entity_chat_id=data.entity_chat_id,
            entity_search_id=data.entity_search_id,
            entity_message_id=data.entity_message_id,
            status=data.status,
            user=data.user,
            keywords=data.keywords.to_dict(),
            searchable=data.chats,
            tariff_plan=data.tariff_plan,
            search_type=data.search_type
        )

    @sync_to_async
    def make_initial(self: None, user: TelegramUser) -> Search:
        return Search.objects.create(user=user)

    @sync_to_async
    def update(self: None, id, **kwargs: any):
        return TelegramUser.objects.filter(telegram_id=id).update(**kwargs)

    @sync_to_async
    def fin_and_update(self: None, id, **kwargs: any) -> tuple[Search, bool]:
        result = TelegramUser.objects.filter(telegram_id=id).update(**kwargs)
        if (result):
            return TelegramUser.objects.filter(telegram_id=id).first()
        return False

    @sync_to_async
    def find(self: None, id: int) -> tuple[Search, bool, None]:
        return Search.objects.filter(id=id).first()    
    
    @sync_to_async
    def delete_if_alowed(self: None, id: int) -> tuple[Search, bool, None]:
        model =  Search.objects.filter(id=id).first()
        
        if model.id:
            return model.delete()
        
        return False

    @sync_to_async
    def exists(self: None, id: int) -> tuple[Search, bool, None]:
        return Search.objects.filter(id=id).exists()

    @sync_to_async
    def getByUser(self: None, user: TelegramUser, status: list):
        query = Search.objects.filter(user=user)

        if (status):
            query = query.filter(status__in=status)

        return SearchRepository.to_list(query.all())
    
    @sync_to_async
    def getByStatus(self: None,  status: str) -> typing.List[Search]:
        sql = Search.objects.filter(status=status).all()
        
        return SearchRepository.to_list(sql)    
    
    @sync_to_async
    def get(self: None,  **filters) -> typing.List[Search]:
        sql = Search.objects.filter(**filters).all()
        
        return SearchRepository.to_list(sql)

    def check_username(name: str) -> bool:
        if isinstance(name, str) and 3 < len(name) < 12 and name[0].isalpha():
            return True
        return False

    @staticmethod
    def get_initial_search(self: None = None):
        return SearchDto()

    @staticmethod
    def get_search_key(id):
        return f'user_search:{id}'
    
    @staticmethod
    def get_new_search_id(self: None = None):
        return random.randint(181, 999)

    @staticmethod
    def get_search_words_key(id, message_id):
        return f'user_search:{id}-keywords:{message_id}'

    @staticmethod
    def set_to_cache(id, data: SearchDto):
        key = SearchRepository.get_search_key(id)
        return Redis().set(key, data.to_dict(), True)

    @staticmethod
    def set_keywords_to_cache(id, m_id, data):
        key = SearchRepository.get_search_words_key(id, m_id)
        return Redis().set(key, data, True)

    @staticmethod
    def get_keywords_from_cache(id, m_id):
        try:
            key = SearchRepository.get_search_words_key(id, m_id)
            return KeywordsDto(Redis().get(key))
        except Exception:
            return KeywordsDto()

    @staticmethod
    def get_search_from_cache(id) -> SearchDto:
        try:
            key = SearchRepository.get_search_key(id)
            return SearchDto(Redis().get(key))
        except Exception:
            return SearchDto()

    @staticmethod
    def remove_search(id):
        key = SearchRepository.get_search_key(id)
        return Redis().delete(key)

    @staticmethod
    def remove_keywords_from_cache(id, message_id):
        key = SearchRepository.get_search_words_key(id, message_id)
        return Redis().delete(key)
