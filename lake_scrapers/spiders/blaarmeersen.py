import os
import re
from datetime import datetime

import scrapy

from lake_scrapers.items import LakeTemperatureItem
from lake_scrapers.pipelines import convert_timestamp


class BlaarmeersenSpider(scrapy.Spider):
    data = {
        "UUID": os.getenv("BLAARMEERSEN_UUID")
    }
    name = 'blaarmeersen'
    allowed_domains = ['bcam.farys.be']
    start_urls = ['https://bcam.farys.be/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs):
        temperature_regex = r"Watertemperatuur\s*\n?\s*(\d+\.\d+)&#8451;"

        timestamp = datetime.now().timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        temperature = re.findall(temperature_regex, response.text)[0]

        uuid = self.data["UUID"]
        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
