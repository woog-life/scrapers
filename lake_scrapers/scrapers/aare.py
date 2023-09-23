import os

import httpx

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class AareScraper(Scraper):
    base_url: str = "https://www.aare-bern.ch"
    paths: list[str] = ["wasserdaten-temperatur"]

    def parse(self, response: httpx.Response) -> LakeTemperatureItem:
        soup = self.soup(response)
        temperature = soup.select_one("#aare-temperature").text.split("°")[0]
        timestamp = soup.select_one("#aare-last-update").text.split("Letztes Update: ")[1]
        timestamp = convert_timestamp(timestamp, time_format="%Y-%m-%d %H:%M:%S")

        uuid = os.getenv("AARE_UUID")

        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
