import sys
import traceback

from lake_scrapers import LakeTemperatureItem
from lake_scrapers import send_data_to_backend, create_logger
from lake_scrapers.scrapers.aare import AareScraper
from lake_scrapers.scrapers.alster import AlsterScraper
from lake_scrapers.scrapers.blaarmeersen import BlaarmeersenScraper
from lake_scrapers.scrapers.cuxhaven import CuxhavenScraper
from lake_scrapers.scrapers.pegelonline import PegelonlineScraper
from lake_scrapers.scrapers.seatemperatureorg import SeaTemperatureOrgScraper
from lake_scrapers.scrapers.woog import WoogScraper


def process_item(item: LakeTemperatureItem, logger):
    temperature = float(item.temperature.replace(",", "."))
    timestamp = item.timestamp
    send_data_to_backend((timestamp, temperature), item.uuid, logger)


SCRAPER_CLASSES = [
    AareScraper,
    AlsterScraper,
    BlaarmeersenScraper,
    CuxhavenScraper,
    PegelonlineScraper,
    SeaTemperatureOrgScraper,
    WoogScraper,
]
# SCRAPER_CLASSES = [WoogSpider]


def main():
    fail = False
    for scraperClass in SCRAPER_CLASSES:
        logger = create_logger(f"scraper_{scraperClass.__name__}")
        scraper = scraperClass()
        for path in scraper.paths:
            try:
                if not scraper.is_allowed_to_scrape(path):
                    logger.error(f"{path}: no")
                    raise Exception(f"not allowed to scrape `{path}`")
                response = scraper.request(path, retry_count=3)
                item = scraper.parse(response)
                process_item(item, logger)
            except Exception as e:
                logger.error(f"failed to process item: {traceback.print_exception(e)}")
                fail = True

    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
