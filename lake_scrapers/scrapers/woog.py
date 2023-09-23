import os

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class WoogScraper(Scraper):
    base_url = "https://woog.iot.service.itrm.de"
    paths = ["?accesstoken=LQ8MXn"]

    def parse(self, response, **kwargs):
        temperature_xpath = "//Water_Temperature/value"
        time_xpath = "//Water_Temperature/ts"

        temperature = self.xpath(temperature_xpath, response, _type="xml")[
            0
        ].text.strip()
        timestamp = self.xpath(time_xpath, response, _type="xml")[0].text.strip()
        timestamp = convert_timestamp(timestamp, is_timestamp_nanosecond=True)

        uuid = os.getenv("LARGE_WOOG_UUID")

        return LakeTemperatureItem(
            temperature=temperature, timestamp=timestamp, uuid=uuid
        )
