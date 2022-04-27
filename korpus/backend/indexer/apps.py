import logging
from django.apps import AppConfig

log = logging.getLogger(__name__)


class IndexerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indexer'
    run_already = False

    def ready(self):
        log.info('Initializing ES connection')
        if IndexerConfig.run_already:
            return
        from indexer import utils
        utils.push_highlighting_limit()
        utils.init_es_connection()
        IndexerConfig.run_already = True
