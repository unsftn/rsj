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


class NinDatesSpider(CrawlSpider):
    name = "nin_dates"
    allowed_domains = ['nin.co.rs']

    archive = ['http://www.nin.co.rs/1999-10/28/index.html',
               #'http://www.nin.co.rs/2000-01/06/index.html',
               #'http://www.nin.co.rs/2000-05/11/index.html',
               #'http://www.nin.co.rs/2000-11/30/index.html',
               #'http://www.nin.co.rs/2001-02/01/index.html',
               #'http://www.nin.co.rs/2001-05/03/index.html',
               #'http://www.nin.co.rs/2001-08/02/index.html',
               #'http://www.nin.co.rs/2001-10/04/index.html',
               #'http://www.nin.co.rs/2001-11/28/index.html',
               #'http://www.nin.co.rs/2002-01/10/index.html',
               #'http://www.nin.co.rs/2002-04/04/index.html',
               #'http://www.nin.co.rs/2002-06/27/index.html',
               #'http://www.nin.co.rs/2002-10/03/index.html',
               #'http://www.nin.co.rs/2002-12/26/index.html',
               #'http://www.nin.co.rs/2003-02/13/index.html',
               #'http://www.nin.co.rs/2003-05/29/index.html',
               #'http://www.nin.co.rs/2003-08/21/index.html'
               # TODO: Neupotrebljivo zbog specijalnih znakova?? npr �lana Predsedni�tva
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

        else:
            pass
