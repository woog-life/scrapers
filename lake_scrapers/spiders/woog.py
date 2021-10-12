import os

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class WoogSpider(scrapy.Spider):
    data = {
        "LQ8MXn": {
            "UUID": os.getenv("LARGE_WOOG_UUID")
        }
    }
    name = 'woog'
    allowed_domains = ['woog.iot.service.itrm.de']
    start_urls = ['https://woog.iot.service.itrm.de/?accesstoken=LQ8MXn']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response, **kwargs):
        temp_xpath = "Water_Temperature/value/text()"
        time_xpath = "Water_Temperature/ts/text()"
        temperature = response.xpath(temp_xpath).get()
        timestamp = response.xpath(time_xpath).get()
        timestamp = convert_timestamp(timestamp, is_timestamp_nanosecond=True)

        url = response.request.url
        accessToken = url.rsplit("=")[-1]
        uuid = self.data[accessToken]["UUID"]

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
