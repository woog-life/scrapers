import os
from datetime import datetime

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class CuxhavenSpider(scrapy.Spider):
    data = {
        "cuxhaven": {
            "UUID": os.getenv("CUXHAVEN_UUID")
        }
    }
    name = 'cuxhaven'
    allowed_domains = ['www.tourlogger.de']
    start_urls = ['https://www.tourlogger.de/wassertemperatur/cuxhaven']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        temp_xpath = ".tourlogger-wassertemperatur::text"
        timestamp = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        temperature = response.css(temp_xpath).get()
        url = response.request.url
        key = url.rsplit("/")[-2]
        uuid = self.data[key]["UUID"]

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
