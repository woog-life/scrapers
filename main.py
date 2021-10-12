from scrapy.crawler import CrawlerProcess

from lake_scrapers.spiders.pegelonline import PegelonlineSpider
from lake_scrapers.spiders.woog import WoogSpider

process = CrawlerProcess()
process.crawl(PegelonlineSpider)
process.crawl(WoogSpider)
process.start()
