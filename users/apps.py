# users/apps.py

from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'
    label = 'users'

    def ready(self):
        import users.signals
