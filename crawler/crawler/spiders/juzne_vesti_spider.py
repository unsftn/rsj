from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.crawler.items import ArticleItem
import sqlite3


conn = sqlite3.connect('crawler.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id integer primary key asc, publisher text, url text NOT NULL UNIQUE)''')
res = c.execute('''SELECT url FROM articles where publisher = "Južne Vesti"''')
final_result = [i[0] for i in res.fetchall()]


class JuzneVestiSpider(CrawlSpider):
    name = "juzne_vesti"
    allowed_domains = ['juznevesti.com']

    archive = ['https://www.juznevesti.com/Arhiva.sr.html?y=2010&m=1&d=19',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2010&m=4&d=23',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2010&m=7&d=28',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2010&m=12&d=5',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2011&m=2&d=7',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2011&m=5&d=16',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2011&m=8&d=24',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2011&m=10&d=4',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2011&m=12&d=22',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2012&m=1&d=19',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2012&m=3&d=9',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2012&m=6&d=27',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2012&m=9&d=7',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2012&m=12&d=28',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2013&m=2&d=6',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2013&m=4&d=25',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2013&m=6&d=27',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2013&m=9&d=3',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2013&m=12&d=28',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2014&m=2&d=28',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2014&m=5&d=10',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2014&m=8&d=31',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2014&m=10&d=17',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2014&m=12&d=22',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2015&m=1&d=6',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2015&m=4&d=23',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2015&m=7&d=2',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2015&m=10&d=4',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2015&m=12&d=11',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2016&m=1&d=5',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2016&m=4&d=7',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2016&m=7&d=31',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2016&m=10&d=30',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2016&m=12&d=16',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2017&m=1&d=25',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2017&m=3&d=3',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2017&m=6&d=29',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2017&m=9&d=13',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2017&m=11&d=30',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2018&m=1&d=18',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2018&m=3&d=31',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2018&m=6&d=5',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2018&m=9&d=15',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2018&m=12&d=1',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2018&m=12&d=1',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2019&m=4&d=25',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2019&m=7&d=18',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2019&m=10&d=11',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2019&m=12&d=20',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2020&m=1&d=9',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2020&m=5&d=11',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2020&m=8&d=1',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2020&m=10&d=28',
               'https://www.juznevesti.com/Arhiva.sr.html?y=2020&m=12&d=6'
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pt10"]/ul//div[@class="article__intro dibvt"]/h3/a'),
             callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        if response.url not in final_result:
            title = response.xpath('//div[@class="article_head"]/h1/text()')[0].get()
            link = response.url
            content = response.xpath('//div[@class="desc_holder cf main--content"]//text()').getall()
            publisher = 'Južne Vesti'
            author = response.xpath('//div[@class="article_head"]/div/span[2]/text()').get()
            date = response.xpath('//p[@class="article--single__date dib color--lgray"]/text()')[1].get().strip()

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
