from aiogram.fsm.state import State, StatesGroup


class GetUsername(StatesGroup):
    get_username = State()
     
class WorkState(StatesGroup):
    chats = State()
    keywords = State()
    doc = State()
    
    
class AdvancedModeState(StatesGroup):
    api_id =State()
    api_hash =State()
    sms_code =State()