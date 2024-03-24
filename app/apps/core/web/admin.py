from django.contrib import admin
from app.apps.core.models import *
# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(SearchTelegramUser)
admin.site.register(Search)
admin.site.register(SearchLead)
admin.site.register(TelegramChat)

admin.site.register(TariffPlan)
