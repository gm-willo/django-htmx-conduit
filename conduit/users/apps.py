from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'conduit.users'
    
    def ready(self):
        import conduit.users.signals
