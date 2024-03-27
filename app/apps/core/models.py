import asgiref.sync
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from app.apps.core.bot.enum import ReviewStatus, SearchStatus, SearchType, UserRole
from asgiref.sync import sync_to_async, async_to_sync


class TariffPlan(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, unique=True)
    is_default = models.BooleanField(default=False)
    group_quantity = models.IntegerField()
    keyword_quantity = models.IntegerField()
    old_messages_offset = models.IntegerField()
    daemon_hours_quantity = models.IntegerField()
    allowed_searches = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.group_quantity} групп'



class SearchTelegramUser(models.Model):
    id=models.AutoField(primary_key=True)
    
    telegram_id = models.CharField(max_length=50,  blank=True, null=True, unique=True)
    api_id = models.CharField(max_length=255, blank=True, null=True)
    api_hash = models.CharField(max_length=255,  blank=True,null=True)
    bot_token =  models.CharField(max_length=255,  blank=True,null=True)
    
    phone = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=80,blank=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    
    auth_code=models.CharField(max_length=50, blank=True, null=True)
    
    name = models.CharField(max_length=50, blank=True, null=True)
    
    is_free = models.BooleanField(default=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    


class TelegramChat(models.Model):
    id=models.AutoField(primary_key=True)
    subscribers = models.ManyToManyField(SearchTelegramUser)
    
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    
    status = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["telegram_id"]
    


class SearchLead(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=80,blank=True)
    
    keywords=models.JSONField()
    
    chats = models.ManyToManyField(TelegramChat, null=True)
    
    
class TelegramUser(models.Model):
    id=models.AutoField(primary_key=True)
    search_accounts= models.ManyToManyField(SearchTelegramUser, blank=True, null=True)
    telegram_username = models.CharField(max_length=80)
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    telegram_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    
    role = models.CharField(max_length=50, blank=True, default=UserRole.USER.value)
    
    tariff_plan = models.ForeignKey(
        TariffPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='telegram_user')
    expired_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        tariff = 'none'
        if(self.tariff_plan):
            tariff = self.tariff_plan.name
            

        mess = '\n' 
        for_messages = {
            'telegram_id':self.telegram_id,
            'telegram_username':self.telegram_username,
            'telegram_name':self.telegram_name,
            'tariff_plan': tariff,
            'last_activity_at':self.last_activity_at,
        }
        
        for key, value in for_messages.items():   
            mess  +=   f"{key}: {value}\n"
            
        return mess


class Debtor(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50,  default=ReviewStatus.REQUESTED) 
    iin_or_bin = models.CharField(max_length=50,  blank=True, null=True, )
    firstname = models.CharField(max_length=50,  blank=True, null=True, )
    lastname = models.CharField(max_length=50,  blank=True, null=True, )
    text = models.CharField(max_length=255,  blank=True, null=True, )

class Search(models.Model):
    SEARCH_STATUSES = (
        ('initial', 'В сбооре'),
        ('ready', 'Ожидает поиска'),
        ('in_process', 'В процессе'),
        ('error', 'Ошибка'),
        ('finished', 'Завершен'),
    )
    leads = models.ManyToManyField(SearchLead, blank=True)
    
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    # По какому тарифному плану производился поиск
    tariff_plan = models.ForeignKey(TariffPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_tariff')
    
    # Расчет на то что поиск будет производиться не только по телеграм группам
    entity_message_id=models.CharField(max_length=255, null=True)
    entity_chat_id=models.CharField(max_length=255, null=True)
    entity_search_id=models.CharField(max_length=255, blank=True, null=True)
    
    keywords=models.JSONField()
    searchable=models.JSONField()
    search_type= models.CharField(max_length=50, default=SearchType.telegram_chats.name)
    
    status = models.CharField(max_length=50, choices=SEARCH_STATUSES, default=SearchStatus.initial.name)
    table_link = models.CharField(max_length=1000, blank=True, null=True)
    searched_at = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @sync_to_async
    def get_user(self):
        return self.user

    
    
    
    def __str__(self) -> str:
        return self.status

    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Search'
