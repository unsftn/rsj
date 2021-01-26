from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.items import ArticleItem
import sqlite3
#import logging


#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
#                    filename='VREME_CMS.log', level=logging.DEBUG)
conn = sqlite3.connect('crawler.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id integer primary key asc, publisher text, url text NOT NULL UNIQUE)''')
res = c.execute('''SELECT url FROM articles where publisher = "Vreme"''')
final_result = [i[0] for i in res.fetchall()]


class VremeSpider(CrawlSpider):
    name = "vreme_cms"
    allowed_domains = ['vreme.com']

    archive = ['https://www.vreme.com/cms/view.php?id=148189',
               'https://www.vreme.com/cms/view.php?id=290974',
               'https://www.vreme.com/cms/view.php?id=291424',
               'https://www.vreme.com/cms/view.php?id=294177',
               'https://www.vreme.com/cms/view.php?id=296790',
               'https://www.vreme.com/cms/view.php?id=299401',
               'https://www.vreme.com/cms/view.php?id=304666',
               'https://www.vreme.com/cms/view.php?id=305288',
               'https://www.vreme.com/cms/view.php?id=312751',
               'https://www.vreme.com/cms/view.php?id=313389',
               'https://www.vreme.com/cms/view.php?id=318385',
               'https://www.vreme.com/cms/view.php?id=322610',
               'https://www.vreme.com/cms/view.php?id=329887',
               'https://www.vreme.com/cms/view.php?id=330154',
               'https://www.vreme.com/cms/view.php?id=343416',
               'https://www.vreme.com/cms/view.php?id=361964',
               'https://www.vreme.com/cms/view.php?id=362541',
               'https://www.vreme.com/cms/view.php?id=381731',
               'https://www.vreme.com/cms/view.php?id=398835',
               'https://www.vreme.com/cms/view.php?id=367834',
               'https://www.vreme.com/cms/view.php?id=387861',
               'https://www.vreme.com/cms/view.php?id=401872',
               'https://www.vreme.com/cms/view.php?id=440007',
               'https://www.vreme.com/cms/view.php?id=451676',
               'https://www.vreme.com/cms/view.php?id=470705',
               'https://www.vreme.com/cms/view.php?id=490476',
               'https://www.vreme.com/cms/view.php?id=507533',
               'https://www.vreme.com/cms/view.php?id=554403',
               'https://www.vreme.com/cms/view.php?id=592002',
               'https://www.vreme.com/cms/view.php?id=635704',
               'https://www.vreme.com/cms/view.php?id=757648',
               'https://www.vreme.com/cms/view.php?id=804637',
               'https://www.vreme.com/cms/view.php?id=869395',
               'https://www.vreme.com/cms/view.php?id=897841',
               'https://www.vreme.com/cms/view.php?id=908296',
               'https://www.vreme.com/cms/view.php?id=928326',
               'https://www.vreme.com/cms/view.php?id=969732',
               'https://www.vreme.com/cms/view.php?id=972477',
               'https://www.vreme.com/cms/view.php?id=1007579',
               'https://www.vreme.com/cms/view.php?id=1024842',
               'https://www.vreme.com/cms/view.php?id=1028927',
               'https://www.vreme.com/cms/view.php?id=1057944',
               'https://www.vreme.com/cms/view.php?id=1086568',
               'https://www.vreme.com/cms/view.php?id=1100814',
               'https://www.vreme.com/cms/view.php?id=1129228',
               'https://www.vreme.com/cms/view.php?id=1152639',
               'https://www.vreme.com/cms/view.php?id=1186937',
               'https://www.vreme.com/cms/view.php?id=1248233',
               'https://www.vreme.com/cms/view.php?id=1259186',
               'https://www.vreme.com/cms/view.php?id=1354215',
               'https://www.vreme.com/cms/view.php?id=1385988',
               'https://www.vreme.com/cms/view.php?id=1438071',
               'https://www.vreme.com/cms/view.php?id=1457030',
               'https://www.vreme.com/cms/view.php?id=1459199',
               'https://www.vreme.com/cms/view.php?id=1460999',
               'https://www.vreme.com/cms/view.php?id=1462921',
               'https://www.vreme.com/cms/view.php?id=1464939',
               'https://www.vreme.com/cms/view.php?id=1472564',
               'https://www.vreme.com/cms/view.php?id=1476205',
               'https://www.vreme.com/cms/view.php?id=1478283',
               'https://www.vreme.com/cms/view.php?id=1480644',
               'https://www.vreme.com/cms/view.php?id=1482663',
               'https://www.vreme.com/cms/view.php?id=1484306',
               'https://www.vreme.com/cms/view.php?id=1484649',
               'https://www.vreme.com/cms/view.php?id=1486562',
               'https://www.vreme.com/cms/view.php?id=1488705',
               'https://www.vreme.com/cms/view.php?id=1490752',
               'https://www.vreme.com/cms/view.php?id=1492546',
               'https://www.vreme.com/cms/view.php?id=1495146',
               'https://www.vreme.com/cms/view.php?id=1496827',
               'https://www.vreme.com/cms/view.php?id=1498517',
               'https://www.vreme.com/cms/view.php?id=1500402',
               'https://www.vreme.com/cms/view.php?id=1501955',
               'https://www.vreme.com/cms/view.php?id=1503627',
               'https://www.vreme.com/cms/view.php?id=1505140',
               'https://www.vreme.com/cms/view.php?id=1506719',
               'https://www.vreme.com/cms/view.php?id=1509801',
               'https://www.vreme.com/cms/view.php?id=1512206',
               'https://www.vreme.com/cms/view.php?id=1513905',
               'https://www.vreme.com/cms/view.php?id=1515453',
               'https://www.vreme.com/cms/view.php?id=1516973',
               'https://www.vreme.com/cms/view.php?id=1518664',
               'https://www.vreme.com/cms/view.php?id=1520083',
               'https://www.vreme.com/cms/view.php?id=1521666',
               'https://www.vreme.com/cms/view.php?id=1523119',
               'https://www.vreme.com/cms/view.php?id=1524590',
               'https://www.vreme.com/cms/view.php?id=1526022',
               'https://www.vreme.com/cms/view.php?id=1527577',
               'https://www.vreme.com/cms/view.php?id=1529210',
               'https://www.vreme.com/cms/view.php?id=1530818',
               'https://www.vreme.com/cms/view.php?id=1532974',
               'https://www.vreme.com/cms/view.php?id=1534917',
               'https://www.vreme.com/cms/view.php?id=1537081',
               'https://www.vreme.com/cms/view.php?id=1539121',
               'https://www.vreme.com/cms/view.php?id=1540646',
               'https://www.vreme.com/cms/view.php?id=1542247',
               'https://www.vreme.com/cms/view.php?id=1542247',
               'https://www.vreme.com/cms/view.php?id=1544837',
               'https://www.vreme.com/cms/view.php?id=1546666',
               'https://www.vreme.com/cms/view.php?id=1549328',
               'https://www.vreme.com/cms/view.php?id=1550948',
               'https://www.vreme.com/cms/view.php?id=1552716',
               'https://www.vreme.com/cms/view.php?id=1554279',
               'https://www.vreme.com/cms/view.php?id=1556530',
               'https://www.vreme.com/cms/view.php?id=1559659',
               'https://www.vreme.com/cms/view.php?id=1559659',
               'https://www.vreme.com/cms/view.php?id=1592636',
               'https://www.vreme.com/cms/view.php?id=1653135',
               'https://www.vreme.com/cms/view.php?id=1676481',
               'https://www.vreme.com/cms/view.php?id=1736663',
               'https://www.vreme.com/cms/view.php?id=1744817',
               'https://www.vreme.com/cms/view.php?id=1769798'
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="mainContent"]//a[text()]'),
             callback='parse_article'),
    )

    def parse_article(self, response):
        if response.url not in final_result:
            title = response.xpath('//head/title/text()').get()
            link = response.url
            unparsed = response.xpath('//div[@id="mainTextClanak"]//p//text()').getall()
            publisher = 'Vreme'
            author = response.xpath('//div[@class="autor"]//text()').get()

            if len(author) < 2:
                author = ""
            else:
                "".join(author).lstrip()

            date = response.xpath('//span[@class="datum"]/text()').get()

            parsed_content = [i.strip() for i in unparsed if i != '\n']
            content = "".join(parsed_content)

            loader = ItemLoader(item=ArticleItem(), response=response)
            loader.add_value('article_title', str(title))
            loader.add_value('article_publisher', str(publisher))
            loader.add_value('article_url', str(link))
            loader.add_value('article_body', content)
            loader.add_value('article_date', str(date.split("|")[2]))
            loader.add_value('article_author', str(author))
            yield loader.load_item()

            c.execute("INSERT INTO articles VALUES (null, ?, ?)", (publisher, str(link)))
            conn.commit()

            #logging.debug('article_url', str(link))
            #logging.debug('article_title', str(title))
            #logging.debug('article_body', content)
            #logging.debug('article_date', str(date.split("|")[2]))
            #logging.debug('article_author', str(author))
            #logging.debug('---------------------------------------\n\n')

        else:
            #logging.info(response.url, " has already been crawled")
            pass
