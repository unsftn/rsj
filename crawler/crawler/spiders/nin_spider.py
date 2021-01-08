from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.crawler.items import ArticleItem
import sqlite3


conn = sqlite3.connect('crawler.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id integer primary key asc, publisher text, url text NOT NULL UNIQUE)''')
res = c.execute('''SELECT url FROM articles where publisher = "НИН - Недељне Информативне Новине"''')
final_result = [i[0] for i in res.fetchall()]


class NinSpider(CrawlSpider):
    name = "nin"
    allowed_domains = ['nin.co.rs']

    archive = ['http://www.nin.co.rs/arhiva/2369/index.html',
               'http://www.nin.co.rs/arhiva/2383/index.html',
               'http://www.nin.co.rs/arhiva/2397/index.html',
               'http://www.nin.co.rs/arhiva/2406/index.html',
               'http://www.nin.co.rs/arhiva/2429/index.html',
               'http://www.nin.co.rs/arhiva/2448/index.html',
               'http://www.nin.co.rs/arhiva/2454/index.html',
               'http://www.nin.co.rs/arhiva/2465/index.html',
               'http://www.nin.co.rs/arhiva/2491/index.html',
               'http://www.nin.co.rs/arhiva/2517/index.html',
               'http://www.nin.co.rs/arhiva/2532/index.html'
               # 72/72 (11 su index-i)
               # TODO: format datuma, i par autora ne valja  (13/72)
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li/a'),
             callback='parse_article', follow=True),

        Rule(LinkExtractor(restrict_xpaths='//body//a', deny='index.html'),
             callback='parse_article', follow=True)
    )

    def parse_article(self, response):
        if response.url not in final_result:
            title = response.xpath('//b/text()').get()
            link = response.url
            unparsed_content = response.xpath('//body//p/text()').getall()
            publisher = 'НИН - Недељне Информативне Новине'
            author = response.xpath('//body/p[last()]/text()').get().strip()

            if author == '':
                author = response.xpath('//body//b/text()')[-1].get()
            else:
                author.strip()

            publication = response.xpath('//body/text()').get().strip().split(",")

            if publication == ['']:
                publication = response.xpath('//head/title/text()').get().split(",")

            pub_num = publication[0]

            if len(publication) > 1:
                pub_date = publication[1]
            else:
                pub_date = ""

            parsed_content = [i.strip() for i in unparsed_content if i != '\n']
            content = "".join(parsed_content[:-1])

            loader = ItemLoader(item=ArticleItem(), response=response)
            loader.add_value('article_title', str(title))
            loader.add_value('article_publisher', str(publisher))
            loader.add_value('article_url', str(link))
            loader.add_value('article_body', content)
            loader.add_value('article_date', pub_date)
            loader.add_value('article_author', str(author[:50]))
            yield loader.load_item()
            c.execute("INSERT INTO articles VALUES (null, ?, ?)", (publisher, str(link)))
            conn.commit()

            #TODO: create publikacija json object and send post request to rsj api
        else:
            pass
