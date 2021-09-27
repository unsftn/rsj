from django.apps import AppConfig


class ReciConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reci'
    verbose_name = 'речи'

    def ready(self):
        import reci.signals
