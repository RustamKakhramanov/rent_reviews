from aiogram.types import Message



def sendReponseToTG(args, func, message: Message):
    message.answer(func())
    
@sendReponseToTG()
def actionSetChat(message: Message):
    return 'Hello world'