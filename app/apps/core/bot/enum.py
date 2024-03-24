from enum import Enum

# class syntax
class SearchStatus(Enum):
    initial = 'В сбооре'
    ready = 'Ожидает поиска'
    in_process = 'В процессе'
    error = 'Ошибка'
    finished = 'Завершен'
    
    
    
class SearchType(Enum):
    telegram_chats = 'Парсинг телеграмм чатов'
    avito = 'Парсинг обьявлений Avito'
    
class UserRole(Enum):
    ADMIN="admin"
    USER="user"
    WRITER="writer"
    REQUEST_WRITER="request_writer"
    