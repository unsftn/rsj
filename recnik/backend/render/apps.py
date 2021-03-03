from django.apps import AppConfig
from django.core.management import call_command

class RenderConfig(AppConfig):
    name = 'render'
    verbose_name = 'рендер'

    def ready(self):
        call_command('migrate', interactive=False, verbosity=0, database='memory')
