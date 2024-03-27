from asgiref.sync import sync_to_async, async_to_sync

from app.apps.core.models import Debtor
from app.apps.core.bot.enum import ReviewStatus
from app.apps.core.repositories.base import BaseRepository


class DebtorRepository:
    @sync_to_async
    def create(self: None, data: dict) -> tuple[Debtor, bool]:
        deb = Debtor.objects.create(
            iin_or_bin=data['iin'],
            firstname=data['firstname'],
            lastname=data['lastname'],
            text=data['review_text'],
            user=data['user'],
            status = data['status'] if 'status' in data else ReviewStatus.REQUESTED
        )
        
        deb.save()
        
        return  deb
    
    @sync_to_async
    def find(self: None, id: int) -> tuple[Debtor, bool, None]:
        return Debtor.objects.filter(id=id).select_related('user').first()
    
    @sync_to_async
    def update_and_find(self: None, id, **kwargs: any):
        result = Debtor.objects.filter(id=id).update(**kwargs)
        if result:
            return Debtor.objects.filter(id=id).select_related('user').first()
        return False
    @sync_to_async
    def delete(self: None, id):
        return Debtor.objects.filter(id=id).delete()
    
    
    @sync_to_async
    def get_by_iin(self: None, iin) -> tuple[Debtor, bool, None]:
        return BaseRepository().to_list(Debtor.objects.filter(iin_or_bin=iin).all())