import os
import re
from datetime import datetime

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


DEFAULT_TEMPERATURE_REGEX = re.compile(
    r"^(?P<temperature>\d+(\.\d+)?).C\s+",
    re.IGNORECASE,
)


class SeaTemperatureOrgScraper(Scraper):
    data = {
        "europe/italy/sorrento.htm": {
            "UUID": os.getenv("SORRENTO_UUID"),
            "regex": DEFAULT_TEMPERATURE_REGEX,
        },
        "europe/spain/santander.htm": {
            "UUID": os.getenv("SANTANDER_UUID"),
            "regex": DEFAULT_TEMPERATURE_REGEX,
        },
        "europe/greece/heraklion.htm": {
            "UUID": os.getenv("HERAKLION_UUID"),
            "regex": DEFAULT_TEMPERATURE_REGEX,
        },
        "north-america/canada/vancouver.htm": {
            "UUID": os.getenv("VANCOUVER_UUID"),
            "regex": DEFAULT_TEMPERATURE_REGEX,
        },
    }

    base_url = "https://www.seatemperature.org"
    paths = [
        "europe/italy/sorrento.htm",
        "europe/spain/santander.htm",
        "europe/greece/heraklion.htm",
        "north-america/canada/vancouver.htm",
    ]

    def parse(self, response, **kwargs):
        path = response.request.url.path.lstrip("/")
        regex = self.data[path]["regex"]
        soup = self.soup(response)
        span = soup.find("div", attrs={"id": "sea-temperature"}).find("span")
        content = span.string.strip()
        matches = regex.search(content)
        temperature = matches.group("temperature")

        timestamp = datetime.now().timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        uuid = self.data[path]["UUID"]
        return LakeTemperatureItem(
            temperature=temperature, timestamp=timestamp, uuid=uuid
        )
