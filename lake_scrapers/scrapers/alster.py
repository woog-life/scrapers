import os

import httpx

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class AlsterScraper(Scraper):
    data = {"clp1": {"UUID": os.getenv("ALSTER_UUID")}}
    base_url = "https://www.hamburg.de"
    paths = ["clp/hu/lombardsbruecke/clp1/"]

    def parse(self, response: httpx.Response):
        soup = self.soup(response)
        temp_xpath = "//td[contains(text(), 'Wassertemperatur')]/../td[3]/text()"
        timestamp_xpath = "//td[contains(text(), 'Wassertemperatur')]/../td[1]/text()"

        temperature = self.xpath(temp_xpath, response)[0].strip()
        timestamp = self.xpath(timestamp_xpath, response)[0].strip()
        timestamp = convert_timestamp(timestamp, time_format="%d.%m.%Y %H:%M")

        path = response.request.url.path
        key = path.rsplit("/")[-2]
        uuid = self.data[key]["UUID"]

        return LakeTemperatureItem(
            temperature=temperature, timestamp=timestamp, uuid=uuid
        )
