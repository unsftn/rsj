from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from crawler.items import ArticleItem


class PolitikaSpider(CrawlSpider):
    name = "politika"
    allowed_domains = ['politika.rs']

    archive = ['http://www.politika.rs/articles/archive/2006/07/27',
               'http://www.politika.rs/articles/archive/2006/09/15',
               'http://www.politika.rs/articles/archive/2006/11/11',
               'http://www.politika.rs/articles/archive/2007/07/26',
               'http://www.politika.rs/articles/archive/2007/02/08',
               'http://www.politika.rs/articles/archive/2007/12/05',
               'http://www.politika.rs/articles/archive/2008/01/03',
               'http://www.politika.rs/articles/archive/2008/06/21',
               'http://www.politika.rs/articles/archive/2008/10/16',
               'http://www.politika.rs/articles/archive/2009/02/25',
               'http://www.politika.rs/articles/archive/2009/08/21',
               'http://www.politika.rs/articles/archive/2009/12/02',
               'http://www.politika.rs/articles/archive/2010/03/25',
               'http://www.politika.rs/articles/archive/2010/08/15',
               'http://www.politika.rs/articles/archive/2010/12/28',
               'http://www.politika.rs/articles/archive/2011/02/12',
               'http://www.politika.rs/articles/archive/2011/04/20',
               'http://www.politika.rs/articles/archive/2011/10/22',
               'http://www.politika.rs/articles/archive/2012/05/11',
               'http://www.politika.rs/articles/archive/2012/08/21',
               'http://www.politika.rs/articles/archive/2012/10/19',
               'http://www.politika.rs/articles/archive/2013/03/07',
               'http://www.politika.rs/articles/archive/2013/06/14',
               'http://www.politika.rs/articles/archive/2013/12/03',
               'http://www.politika.rs/articles/archive/2014/01/16',
               'http://www.politika.rs/articles/archive/2014/06/10',
               'http://www.politika.rs/articles/archive/2014/12/20',
               'http://www.politika.rs/articles/archive/2015/01/15',
               'http://www.politika.rs/articles/archive/2015/07/21',
               'http://www.politika.rs/articles/archive/2015/10/03',
               'http://www.politika.rs/articles/archive/2016/02/29',
               'http://www.politika.rs/articles/archive/2016/08/09',
               'http://www.politika.rs/articles/archive/2016/12/08',
               'http://www.politika.rs/articles/archive/2017/05/22',
               'http://www.politika.rs/articles/archive/2017/09/02',
               'http://www.politika.rs/articles/archive/2017/12/31',
               'http://www.politika.rs/articles/archive/2018/03/15',
               'http://www.politika.rs/articles/archive/2018/06/07',
               'http://www.politika.rs/articles/archive/2018/09/13',
               'http://www.politika.rs/articles/archive/2019/03/21',
               'http://www.politika.rs/articles/archive/2019/08/05',
               'http://www.politika.rs/articles/archive/2019/10/11',
               'http://www.politika.rs/articles/archive/2020/02/07',
               'http://www.politika.rs/articles/archive/2020/06/06',
               'http://www.politika.rs/articles/archive/2020/10/18'
               ]

    start_urls = []
    for link in archive:
        for i in range(1, 10):
            start_urls.append(link + '/page:' + str(i))

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="archive-list"]/div/div/div/a'),
             callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        title = response.xpath('//head/title/text()')[0].get()
        link = response.url
        content = "".join(response.xpath('//article//div[contains(@class, "article-content")]//text()').getall()).splitlines()
        publisher = 'Politika'
        author = response.xpath('//article//div[contains(@class, "date-time")]/a[contains(@class,"author-name")]/text()').get()
        date = response.xpath('//article//div[contains(@class, "date-time")]/text()').get().strip()

        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_value('article_title', str(title))
        loader.add_value('article_publisher', str(publisher))
        loader.add_value('article_url', str(link))
        loader.add_value('article_body', str("".join(content).lstrip()))
        loader.add_value('article_date', str(date))
        loader.add_value('article_author', str(author))
        yield loader.load_item()
