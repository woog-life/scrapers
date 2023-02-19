import os
from datetime import datetime

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class SeaTemperatureInfoSpider(scrapy.Spider):
    data = {
        "de/spanien/santander-wassertemperatur.html": {
            "UUID": os.getenv("SANTANDER_UUID"),
            "xpath": "//tr[td='heute']/../tr[2]/td//text()"
        },
        "heraklion-water-temperature.html": {
            "UUID": os.getenv("HERAKLION_UUID"),
            "xpath": "//tr[td='today temp']/../tr[2]/td//text()"
        }
    }
    name = 'seatemperatureinfo'
    allowed_domains = ['seatemperature.info']
    base_url = "https://seatemperature.info"

    def start_requests(self):
        for path in self.data.keys():
            url = "/".join([self.base_url, path])
            yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        url = response.request.url
        path = url.replace(self.base_url + "/", "")
        temp_xpath = self.data[path]["xpath"]
        temperature = response.xpath(temp_xpath).get()

        timestamp = datetime.now().timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        uuid = self.data[path]["UUID"]
        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
