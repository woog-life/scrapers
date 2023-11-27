import os
import re
from datetime import datetime

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class SeaTemperatureInfoScraper(Scraper):
    data = {
        "de/spanien/santander-wassertemperatur.html": {
            "UUID": os.getenv("SANTANDER_UUID"),
            "regex": re.compile(
                r"Die Wassertemperatur in Santander beträgt heute (?P<temperature>\d+(\.\d+)?)",
                re.IGNORECASE,
            ),
        },
        "heraklion-water-temperature.html": {
            "UUID": os.getenv("HERAKLION_UUID"),
            "regex": re.compile(
                r"Water temperature in Heraklion today is (?P<temperature>\d+(\.\d+)?)",
                re.IGNORECASE,
            ),
        },
        "vancouver-water-temperature.html": {
            "UUID": os.getenv("VANCOUVER_UUID"),
            "regex": re.compile(
                r"Water temperature in Vancouver today is (?P<temperature>\d+(\.\d+)?)",
                re.IGNORECASE,
            ),
        },
        "italy/sorrento-water-temperature.html": {
            "UUID": os.getenv("SORRENTO_UUID"),
            "regex": re.compile(
                r"Water temperature in Sorrento today is (?P<temperature>\d+(\.\d+)?)",
                re.IGNORECASE,
            ),
        },
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    }

    base_url = "https://seatemperature.info"
    paths = [
        "de/spanien/santander-wassertemperatur.html",
        "heraklion-water-temperature.html",
        "vancouver-water-temperature.html",
        "italy/sorrento-water-temperature.html",
    ]

    def parse(self, response, **kwargs):
        path = response.request.url.path.lstrip("/")
        regex = self.data[path]["regex"]
        content: str = response.text
        matches = regex.search(content)
        temperature = matches.group("temperature")

        timestamp = datetime.now().timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        uuid = self.data[path]["UUID"]
        return LakeTemperatureItem(
            temperature=temperature, timestamp=timestamp, uuid=uuid
        )
