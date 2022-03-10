from django.apps import AppConfig


class PublikacijeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publikacije'
    verbose_name = 'публикације'

    def ready(self):
        import publikacije.signals
