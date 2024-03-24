

from abc import abstractmethod
from app.apps.core.models import Search
from typing import List
from app.apps.core.DTO import SearchDto
from app.services.has_attributes import HasAttributes
from telethon import TelegramClient
from app.apps.core.models import Search
from app.apps.core.DTO import SearchDto

class BaseClient:
    pass


class HasSearchEntities(HasAttributes):
    telegram_client: TelegramClient = None
    searches:List[Search]| List[SearchDto] = None
    
    def __init__(self, **args) -> None:
        self.set_attributes(args)
        
