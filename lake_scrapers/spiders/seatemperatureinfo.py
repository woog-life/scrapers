import os
import re
from datetime import datetime

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class SeaTemperatureInfoSpider(scrapy.Spider):
    data = {
        "de/spanien/santander-wassertemperatur.html": {
            "UUID": os.getenv("SANTANDER_UUID"),
            "regex": re.compile(r"Die Wassertemperatur in Santander beträgt heute (?P<temperature>\d+(\.\d+)?)"),
        },
        "heraklion-water-temperature.html": {
            "UUID": os.getenv("HERAKLION_UUID"),
            "regex": re.compile(r"Water temperature in Heraklion today is (?P<temperature>\d+(\.\d+)?)"),
        }
    }
    name = 'seatemperatureinfo'
    allowed_domains = ['seatemperature.info']
    base_url = "https://seatemperature.info"

    def start_requests(self):
        for path in self.data.keys():
            url = "/".join([self.base_url, path])
            yield scrapy.Request(url, self.parse, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
            })

    def parse(self, response, **kwargs):
        url = response.request.url
        path = url.replace(self.base_url + "/", "")
        regex = self.data[path]["regex"]
        content: str = response.text
        matches = regex.search(content)
        temperature = matches.group("temperature")

        timestamp = datetime.now().timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        uuid = self.data[path]["UUID"]
        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
