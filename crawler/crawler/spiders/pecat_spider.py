from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.crawler.items import ArticleItem
import sqlite3


conn = sqlite3.connect('crawler.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id integer primary key asc, publisher text, url text NOT NULL UNIQUE)''')
res = c.execute('''SELECT url FROM articles where publisher = "Печат"''')
final_result = [i[0] for i in res.fetchall()]


class PecatSpider(CrawlSpider):
    name = "pecat"
    allowed_domains = ['pecat.co.rs']

    archive = ['http://www.pecat.co.rs/category/broj-301/',
               'http://www.pecat.co.rs/category/broj-310/',
               'http://www.pecat.co.rs/category/broj-325/',
               'http://www.pecat.co.rs/category/broj-336/',
               'http://www.pecat.co.rs/category/broj-348/',
               'http://www.pecat.co.rs/category/broj-355/',
               'http://www.pecat.co.rs/category/broj-364/',
               'http://www.pecat.co.rs/category/broj-378/',
               'http://www.pecat.co.rs/category/broj-390/',
               'http://www.pecat.co.rs/category/broj-402/',
               'http://www.pecat.co.rs/category/broj-405/',
               'http://www.pecat.co.rs/category/broj-419/',
               'http://www.pecat.co.rs/category/broj-426/',
               'http://www.pecat.co.rs/category/broj-434/',
               'http://www.pecat.co.rs/category/broj-447/',
               'http://www.pecat.co.rs/category/broj-453/',
               'http://www.pecat.co.rs/category/broj-464/',
               'http://www.pecat.co.rs/category/broj-470/',
               'http://www.pecat.co.rs/category/broj-481/',
               'http://www.pecat.co.rs/category/broj-491/',
               'http://www.pecat.co.rs/category/broj-505/',
               'http://www.pecat.co.rs/category/broj-517/',
               'http://www.pecat.co.rs/category/broj-531/',
               'http://www.pecat.co.rs/category/broj-539/',
               'http://www.pecat.co.rs/category/broj-548/',
               'http://www.pecat.co.rs/category/broj-552/',
               'http://www.pecat.co.rs/category/broj-559/',
               'http://www.pecat.co.rs/category/broj-574/',
               'http://www.pecat.co.rs/category/broj-584/',
               'http://www.pecat.co.rs/category/broj-594/',
               'http://www.pecat.co.rs/category/broj-600/',
               'http://www.pecat.co.rs/category/broj-608/',
               'http://www.pecat.co.rs/category/broj-614/',
               'http://www.pecat.co.rs/category/broj-620/',
               'http://www.pecat.co.rs/category/broj-634/',
               'http://www.pecat.co.rs/category/broj-643/'
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="post-listing archive-box"]/article/div[@class="entry"]/a'),
             callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        if response.url not in final_result:
            title = response.xpath('//div[@class="content"]/article/div/h1/span/text()').get()
            link = response.url
            unparsed = response.xpath('//div[@class="content"]/article/div/div[@class="entry"]//text()').getall()
            publisher = 'Печат'
            author = response.xpath('//div[@class="content"]/article/div/p[@class="post-meta"]/span[@class="post-meta-author"]/a/text()').get().strip()
            date = response.xpath('//div[@class="content"]/article/div/p[@class="post-meta"]/span[@class="tie-date"]/text()').get().strip()

            parsed_content = [i.strip() for i in unparsed if i != '\n']
            content = "".join(parsed_content[3:-1])

            loader = ItemLoader(item=ArticleItem(), response=response)
            loader.add_value('article_title', str(title))
            loader.add_value('article_publisher', str(publisher))
            loader.add_value('article_url', str(link))
            loader.add_value('article_body', str("".join(content).lstrip()))
            loader.add_value('article_date', str(date))
            loader.add_value('article_author', str(author))
            yield loader.load_item()

            c.execute("INSERT INTO articles VALUES (null, ?, ?)", (publisher, str(link)))
            conn.commit()

        else:
            pass