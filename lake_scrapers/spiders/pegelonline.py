import os

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class PegelonlineSpider(scrapy.Spider):
    data = {
        "580412": {
            "UUID": os.getenv("POTSDAM_UUID")
        },
        "2730010": {
            "UUID": os.getenv("COLOGNE_UUID")
        }
    }
    name = 'pegelonline'
    allowed_domains = ['www.pegelonline.wsv.de']
    start_urls = ['https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=2730010',
                  'https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=580412']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        temp_xpath = "//td[contains(text(), 'Wassertemperatur')]/../*[2]//text()"
        time_xpath = "//td[contains(text(), 'Wassertemperatur')]/../*[3]//text()"
        temperature = response.xpath(temp_xpath).get()
        timestamp = response.xpath(time_xpath).get()
        timestamp = convert_timestamp(timestamp)

        url = response.request.url
        pegelnr = url.rsplit("=")[-1]
        uuid = self.data[pegelnr]["UUID"]

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
