from django.apps import AppConfig
from django.core.management import call_command


class RenderConfig(AppConfig):
    name = 'render'
    verbose_name = 'рендер'

    def ready(self):
        call_command('migrate', interactive=False, verbosity=0, database='memory')
        call_command('loaddata', 'start_groups', 'start_users', 'vrste_publikacija',
                     'operacije-izmene', 'status_odrednice', 'renderi', verbosity=0, database='memory')
        call_command('copycoders', verbosity=0)
