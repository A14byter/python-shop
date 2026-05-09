from django.contrib import admin

from .models import Account,AccountComplete,Notification

admin.site.register(Account)
admin.site.register(AccountComplete)
admin.site.register(Notification)