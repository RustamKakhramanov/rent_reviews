import app.apps.core.DTO
import app.apps.core.models
import asgiref.sync
import json
from typing import *

from app.apps.core.models import *
from app.apps.core.DTO import ChatsWithOrdersDto, SearchOrderDTO
from asgiref.sync import sync_to_async, async_to_sync


class EntitiesMaker:

    @sync_to_async
    def make_unique_chats_with_orders(self: None, searches: List[Search]):
        result: List[ChatsWithOrdersDto] = []

        def is_unique_user(result: List[ChatsWithOrdersDto], chat_id, user: TelegramUser):
            return not any(
                order.user.id == user.id for chat in result
                if chat.chat_id == chat_id for order in chat.orders
            )

        def is_unique_chat(result: List[ChatsWithOrdersDto], searchable):
            return not any(res_item.chat_id == searchable for res_item in result)

        for search in searches:
            order = SearchOrderDTO({
                'keywords': search.keywords,
                'user':   (search.user)
            })

            for searchable in search.searchable:
                if is_unique_chat(result, searchable) and is_unique_user(result, searchable,  order.user):
                    result.append(
                        ChatsWithOrdersDto({
                            'chat_id': searchable,
                            'orders': [order]
                        })
                    )

                elif not is_unique_chat(result, searchable) and is_unique_user(result, searchable,  order.user):
                    for res_item in result:
                        if res_item.chat_id == searchable:
                            res_item.orders.append(order)

        return result


# Dump Example

#  [
#                 {
#                     'chat_id': -1001254870708,
#                     'orders': [
#                         {'keywords': {'name': 'Nzbdbdnd', 'options': [
#                             'Xbxnxnxn', 'Shxnxnxndn', 'Dbxnxbbxbd', 'Xnxnbdbdbdnd']}, 'user': 8},
#                         {'keywords': {'name': 'Shvabraide', 'options': ['Siks', 'Doner', 'skills', 'Kebab']}, 'user': 9}]},
#                 {
#                     'chat_id': -1001449848668,
#                     'orders': [
#                         {
#                             'keywords':
#                                 {
#                                     'name': 'Nzbdbdnd',
#                                     'options': [
#                                         'Xbxnxnxn',
#                                         'Shxnxnxndn',
#                                         'Dbxnxbbxbd',
#                                         'Xnxnbdbdbdnd'
#                                     ]
#                                 },
#                                 'user': 8
#                         },
#                         {
#                             'keywords': {
#                                 'name': 'Shvabraide',
#                                 'options': ['Siks', 'Doner', 'skills', 'Kebab']
#                             }, 'user': 9}
#                     ]
#                 },
#                 {
#                     'chat_id': -1001762602368,
#                     'orders': [{'keywords': {'name': 'Nzbdbdnd', 'options': ['Xbxnxnxn', 'Shxnxnxndn', 'Dbxnxbbxbd', 'Xnxnbdbdbdnd']}, 'user': 8},
#                                {'keywords': {'name': 'Shvabraide', 'options': [
#                                    'Siks', 'Doner', 'skills', 'Kebab']}, 'user': 9}
#                                ]
#                 },
#                 {
#                     'chat_id': -1001447848668,
#                     'orders': [{'keywords': {'name': 'Shvabraide', 'options': ['Siks', 'Doner', 'skills', 'Kebab']}, 'user': 9}]
#                 }
#             ]
