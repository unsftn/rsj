# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class ArticleItem(Item):
    article_title = Field()
    article_publisher = Field()
    article_url = Field()
    article_body = Field()
    article_date = Field()
    article_author = Field()
