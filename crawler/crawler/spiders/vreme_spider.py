from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.crawler.items import ArticleItem


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
               'https://www.vreme.com/arhiva_html/530/sadrzaj.html',
               # 'https://www.vreme.com/cms/view.php?id=148189',
               # 'https://www.vreme.com/cms/view.php?id=290974',
               # 'https://www.vreme.com/cms/view.php?id=291424',
               # 'https://www.vreme.com/cms/view.php?id=294177',
               # 'https://www.vreme.com/cms/view.php?id=296790',
               # 'https://www.vreme.com/cms/view.php?id=299401',
               # 'https://www.vreme.com/cms/view.php?id=304666',
               # 'https://www.vreme.com/cms/view.php?id=305288',
               # 'https://www.vreme.com/cms/view.php?id=312751',
               # 'https://www.vreme.com/cms/view.php?id=313389',
               # 'https://www.vreme.com/cms/view.php?id=318385',
               # 'https://www.vreme.com/cms/view.php?id=322610',
               # 'https://www.vreme.com/cms/view.php?id=329887',
               # 'https://www.vreme.com/cms/view.php?id=330154',
               # 'https://www.vreme.com/cms/view.php?id=343416',
               # 'https://www.vreme.com/cms/view.php?id=361964',
               # 'https://www.vreme.com/cms/view.php?id=362541',
               # 'https://www.vreme.com/cms/view.php?id=381731',
               # 'https://www.vreme.com/cms/view.php?id=398835',
               # 'https://www.vreme.com/cms/view.php?id=367834',
               # 'https://www.vreme.com/cms/view.php?id=387861',
               # 'https://www.vreme.com/cms/view.php?id=401872',
               # 'https://www.vreme.com/cms/view.php?id=440007',
               # 'https://www.vreme.com/cms/view.php?id=451676',
               # 'https://www.vreme.com/cms/view.php?id=470705',
               # 'https://www.vreme.com/cms/view.php?id=490476',
               # 'https://www.vreme.com/cms/view.php?id=507533',
               # 'https://www.vreme.com/cms/view.php?id=554403',
               # 'https://www.vreme.com/cms/view.php?id=592002',
               # 'https://www.vreme.com/cms/view.php?id=635704',
               # 'https://www.vreme.com/cms/view.php?id=757648',
               # 'https://www.vreme.com/cms/view.php?id=804637',
               # 'https://www.vreme.com/cms/view.php?id=869395',
               # 'https://www.vreme.com/cms/view.php?id=897841',
               # 'https://www.vreme.com/cms/view.php?id=908296',
               # 'https://www.vreme.com/cms/view.php?id=928326',
               # 'https://www.vreme.com/cms/view.php?id=969732',
               # 'https://www.vreme.com/cms/view.php?id=972477',
               # 'https://www.vreme.com/cms/view.php?id=1007579',
               # 'https://www.vreme.com/cms/view.php?id=1024842',
               # 'https://www.vreme.com/cms/view.php?id=1028927',
               # 'https://www.vreme.com/cms/view.php?id=1057944',
               # 'https://www.vreme.com/cms/view.php?id=1086568',
               # 'https://www.vreme.com/cms/view.php?id=1100814',
               # 'https://www.vreme.com/cms/view.php?id=1129228',
               # 'https://www.vreme.com/cms/view.php?id=1152639',
               # 'https://www.vreme.com/cms/view.php?id=1186937',
               # 'https://www.vreme.com/cms/view.php?id=1248233',
               # 'https://www.vreme.com/cms/view.php?id=1259186',
               # 'https://www.vreme.com/cms/view.php?id=1354215',
               # 'https://www.vreme.com/cms/view.php?id=1385988',
               # 'https://www.vreme.com/cms/view.php?id=1438071',
               # 'https://www.vreme.com/arhiva.php?year=2017',
               # 'https://www.vreme.com/cms/view.php?id=1559659',
               # 'https://www.vreme.com/cms/view.php?id=1592636',
               # 'https://www.vreme.com/cms/view.php?id=1653135',
               # 'https://www.vreme.com/cms/view.php?id=1676481',
               # 'https://www.vreme.com/cms/view.php?id=1736663',
               # 'https://www.vreme.com/cms/view.php?id=1744817',
               # 'https://www.vreme.com/cms/view.php?id=1769798'
               ]

    start_urls = []
    for link in archive:
        start_urls.append(link)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a'),
             callback='parse_article'),
    )

    def parse_article(self, response):
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
