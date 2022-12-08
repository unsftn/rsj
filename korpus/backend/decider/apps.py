from django.apps import AppConfig


class DeciderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'decider'
    verbose_name = 'одлуке'

    def ready(self):
        import decider.signals
