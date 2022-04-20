from django.apps import AppConfig
from .utils import push_highlighting_limit


class IndexerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indexer'

    def ready(self):
        push_highlighting_limit()
