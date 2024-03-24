

from telethon import TelegramClient
from app.apps.core.DTO import SearchTelegramAccount
from app.apps.core.repositories.search_telegram_user import SearchTelehramUserRepository
import asyncio


async def init_and_start():
    data:SearchTelegramAccount =  await SearchTelehramUserRepository.findFree()
    client =  TelegramClient(data.username, int(data.api_id), data.api_hash, system_version="4.16.30-vxCUSTOM") 
    await client.start(phone=data.phone)
    return client



    
# Iterations Untill disconnect
def telegram_daemon():
    def wrapper(func):
        async def wrapped(obj, **args):
            client:TelegramClient = await init_and_start()
            await func(self=obj, client=client, **args)
            await client.run_until_disconnected()
        return wrapped
    return wrapper
    


# One iteration
def telegram_iteration():
    def wrapper(func):
        async def wrapped(obj, **args):
            client:TelegramClient = await init_and_start()
            await func(self=obj, client=client, **args)
            await client.disconnect()
        return wrapped
    return wrapper



#client = TelegramClient(None, api_id, api_hash)
# client.session.set_dc(2, '149.154.167.40', 80)
# client.start(
#     phone='9996621234', code_callback=lambda: '22222'
# )

# https://docs.telethon.dev/en/stable/developing/test-servers.html