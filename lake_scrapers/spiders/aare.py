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
        temp_xpath = response.xpath("//temp/text()").get().split("°")[0]
        timestamp_xpath = response.xpath("//temp-normal/text()").get().split("Letztes Update: ")[1]

        temperature = response.xpath(temp_xpath).get().strip()
        timestamp = response.xpath(timestamp_xpath).get().strip()
        timestamp = convert_timestamp(timestamp, time_format="%Y-%m-%d %H:%M:%S")

        url = response.request.url
        key = url.rsplit("/")[-2]
        uuid = os.getenv("AARE_UUID")

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
