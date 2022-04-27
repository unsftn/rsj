import logging
from django.apps import AppConfig

log = logging.getLogger(__name__)


class IndexerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indexer'

    def ready(self):
        from indexer import utils
        utils.push_highlighting_limit()
