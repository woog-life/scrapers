from scrapy.crawler import CrawlerProcess

from lake_scrapers.spiders.aare import AareSpider
from lake_scrapers.spiders.alster import AlsterSpider
from lake_scrapers.spiders.cuxhaven import CuxhavenSpider
from lake_scrapers.spiders.pegelonline import PegelonlineSpider
from lake_scrapers.spiders.woog import WoogSpider

process = CrawlerProcess()
process.crawl(PegelonlineSpider)
process.crawl(WoogSpider)
process.crawl(CuxhavenSpider)
process.crawl(AlsterSpider)
process.crawl(AareSpider)
process.start()
