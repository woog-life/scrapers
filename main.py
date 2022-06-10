from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from lake_scrapers.spiders.aare import AareSpider
from lake_scrapers.spiders.alster import AlsterSpider
from lake_scrapers.spiders.cuxhaven import CuxhavenSpider
from lake_scrapers.spiders.pegelonline import PegelonlineSpider
from lake_scrapers.spiders.woog import WoogSpider

crawlers = [PegelonlineSpider, WoogSpider, CuxhavenSpider, AlsterSpider, AareSpider]

settings = get_project_settings()
runner = CrawlerRunner(settings)
for crawler in crawlers:
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(crawler)
    # process.start()
    runner.crawl(crawler)

d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
