import os

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class AlsterSpider(scrapy.Spider):
    data = {
        "clp1": {
            "UUID": os.getenv("ALSTER_UUID")
        }
    }
    name = 'alster'
    allowed_domains = ['www.hamburg.de']
    start_urls = ['https://www.hamburg.de/clp/hu/lombardsbruecke/clp1/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        temp_xpath = "//td[contains(text(), 'Wassertemperatur')]/../td[3]/text()"
        timestamp_xpath = "//td[contains(text(), 'Wassertemperatur')]/../td[1]/text()"

        temperature = response.xpath(temp_xpath).get().strip()
        timestamp = response.xpath(timestamp_xpath).get().strip()
        timestamp = convert_timestamp(timestamp, time_format="%d.%m.%Y %H:%M")

        url = response.request.url
        key = url.rsplit("/")[-2]
        uuid = self.data[key]["UUID"]

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
