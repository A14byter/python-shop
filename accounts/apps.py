from django.apps import AppConfig
from django.db import connection

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # فعال‌سازی foreign_keys در SQLite
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys=ON;')