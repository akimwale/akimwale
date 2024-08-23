from django.apps import AppConfig


class TeluskoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telusko_app'

def ready(self):
        import accounts.signals
