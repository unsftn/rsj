# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from datetime import datetime
from hashlib import md5
from twisted.enterprise import adbapi




class MySQLStorePipeline(object):
    """
    A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            port='3309',
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        print("!!!!!!!!!!! trying to process the item !!!!!!!!!!!!")
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        # guid = self._get_guid(item)
        # now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        print("!!!!!!!!!!! trying to upsert !!!!!!!!!!!!")
        res = conn.execute(
            "INSERT INTO publication (naslov, clanak, url, izdavac, godina, autor) VALUES (%s, %s, %s, %s, %s, %s) ",
            (item['article_title'][0],
             item['article_body'][0],
             item['article_url'][0],
             item['article_publisher'][0],
             item['article_date'][0],
             item['article_author'][0]))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        self.log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
