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


class NinPagesSpider(CrawlSpider):
    name = "nin_pages"
    allowed_domains = ['nin.co.rs']

    archive = [ 'http://www.nin.co.rs/pages/issue.php?id=596',
                'http://www.nin.co.rs/pages/issue.php?id=612',
                'http://www.nin.co.rs/pages/issue.php?id=618',
                'http://www.nin.co.rs/pages/issue.php?id=640',
                'http://www.nin.co.rs/pages/issue.php?id=660',
                'http://www.nin.co.rs/pages/issue.php?id=692',
                'http://www.nin.co.rs/pages/issue.php?id=716',
                'http://www.nin.co.rs/pages/issue.php?id=720',
                'http://www.nin.co.rs/pages/issue.php?id=754',
                'http://www.nin.co.rs/pages/issue.php?id=774',
                'http://www.nin.co.rs/pages/issue.php?id=788',
                'http://www.nin.co.rs/pages/issue.php?id=816',
                'http://www.nin.co.rs/pages/issue.php?id=826',
                'http://www.nin.co.rs/pages/issue.php?id=850',
                'http://www.nin.co.rs/pages/issue.php?id=878',
                'http://www.nin.co.rs/pages/issue.php?id=27615',
                'http://www.nin.co.rs/pages/issue.php?id=27930',
                'http://www.nin.co.rs/pages/issue.php?id=29027',
                'http://www.nin.co.rs/pages/issue.php?id=29043',
                'http://www.nin.co.rs/pages/issue.php?id=31734',
                'http://www.nin.co.rs/pages/issue.php?id=33913',
                'http://www.nin.co.rs/pages/issue.php?id=34967',
                'http://www.nin.co.rs/pages/issue.php?id=36160',
                'http://www.nin.co.rs/pages/issue.php?id=37598',
                'http://www.nin.co.rs/pages/issue.php?id=39496',
                'http://www.nin.co.rs/pages/issue.php?id=40475',
                'http://www.nin.co.rs/pages/issue.php?id=41900',
                'http://www.nin.co.rs/pages/issue.php?id=42028',
                'http://www.nin.co.rs/pages/issue.php?id=43047',
                'http://www.nin.co.rs/pages/issue.php?id=44422',
                'http://www.nin.co.rs/pages/issue.php?id=46547',
                'http://www.nin.co.rs/pages/issue.php?id=48052',
                'http://www.nin.co.rs/pages/issue.php?id=49571',
                'http://www.nin.co.rs/pages/issue.php?id=52027',
                'http://www.nin.co.rs/pages/issue.php?id=54465',
                'http://www.nin.co.rs/pages/issue.php?id=56938',
                'http://www.nin.co.rs/pages/issue.php?id=58079',
                'http://www.nin.co.rs/pages/issue.php?id=58351',
                'http://www.nin.co.rs/pages/issue.php?id=59966',
                'http://www.nin.co.rs/pages/issue.php?id=61557',
                'http://www.nin.co.rs/pages/issue.php?id=62932'
               # TODO: samo besplatni clanci su moguci (3 po stranici))
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//body//tbody/tr/td[@width="278"]//a'),
             callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        if response.url not in final_result:
            title = response.xpath('//head/meta[@property="og:title"]/@content').get()
            link = response.url
            unparsed_content = response.xpath('//table[@style="table-layout:fixed"]//text()').getall()
            publisher = 'НИН - Недељне Информативне Новине'
            author = response.xpath('(//td/b)[last()]/text()').get()

            if author is None:
                author = response.xpath('//span[@class="izjava"]/b/text()').get()

            if author is None:
                author = response.xpath('//strong//text()').get()

            if author is None:
                author = ""

            publication = response.xpath('//div[@align="center"]//a/text()').get().split(",")
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
