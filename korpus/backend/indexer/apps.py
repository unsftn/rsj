import logging
import sys
from django.apps import AppConfig

log = logging.getLogger(__name__)


class IndexerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indexer'

    def ready(self):
        if sys.argv[-1] not in ['runserver', 'korpus.wsgi:application']:
            return
        # from indexer import utils
        # utils.push_highlighting_limit()
        # log.info('Highligting limit pushed to Elasticsearch.')
