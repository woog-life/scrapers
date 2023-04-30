import os

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class AareSpider(scrapy.Spider):
    name = 'aare'
    allowed_domains = ['www.aare-bern.ch']
    start_urls = ['https://www.aare-bern.ch/wasserdaten-temperatur/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        temperature = response.css("#aare-temperature")[0].root.text.split("°")[0]
        timestamp = response.css("temp-normal::text").get().split("Letztes Update: ")[1]
        timestamp = convert_timestamp(timestamp, time_format="%Y-%m-%d %H:%M:%S")

        uuid = os.getenv("AARE_UUID")

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
