from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.items import ArticleItem
import sqlite3


conn = sqlite3.connect('crawler.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id integer primary key asc, publisher text, url text NOT NULL UNIQUE)''')
res = c.execute('''SELECT url FROM articles where publisher = "Vreme"''')
final_result = [i[0] for i in res.fetchall()]


class VremeSpider(CrawlSpider):
    name = "vreme"
    allowed_domains = ['vreme.com']

    archive = ['https://www.vreme.com/arhiva_html/427/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/432/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/436/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/vb3/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/vb7/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/vb10/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/440/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/445/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/449/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/454/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/460/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/468/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/469/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/479/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/489/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/495/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/505/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/514/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/521/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/522/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/526/sadrzaj.html',
               'https://www.vreme.com/arhiva_html/530/sadrzaj.html'
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a'),
             callback='parse_article'),
    )

    def parse_article(self, response):
        if response.url not in final_result:
            title = response.xpath('//table/tr//p[@class="naslov"]/text()').get()
            link = response.url
            unparsed = response.xpath('//table//tr//p/text()').getall()
            publisher = 'Vreme'
            author = response.xpath('//table//em/text()').get()

            if author is None:
                author = ",".join(response.xpath('//table/tr/td//p[last()]/text()').getall()).splitlines()

            date = response.xpath('//table/tr/td[@align="right"]/p//text()').get()

            parsed_content = [i.strip() for i in unparsed if i != '\n']
            content = "".join(parsed_content[2:])

            loader = ItemLoader(item=ArticleItem(), response=response)
            loader.add_value('article_title', str(title))
            loader.add_value('article_publisher', str(publisher))
            loader.add_value('article_url', str(link))
            loader.add_value('article_body', content)
            loader.add_value('article_date', str(date))
            loader.add_value('article_author', str("".join(author).lstrip()))
            yield loader.load_item()

            c.execute("INSERT INTO articles VALUES (null, ?, ?)", (publisher, str(link)))
            conn.commit()
        else:
            pass
