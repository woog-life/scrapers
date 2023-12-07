import os
import re
from datetime import datetime

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class SeaTemperatureOrgScraper(Scraper):
    data = {
        "europe/italy/sorrento.htm": {
            "UUID": os.getenv("SORRENTO_UUID"),
            "regex": re.compile(
                r"^(?P<temperature>\d+(\.\d+)?).C\s+",
                re.IGNORECASE,
            ),
        },
        "europe/spain/santander.htm": {
            "UUID": os.getenv("SANTANDER_UUID"),
            "regex": re.compile(
                r"^(?P<temperature>\d+(\.\d+)?).C\s+",
                re.IGNORECASE,
            ),
        },
        "europe/greece/heraklion.htm": {
            "UUID": os.getenv("HERAKLION_UUID"),
            "regex": re.compile(
                r"^(?P<temperature>\d+(\.\d+)?).C\s+",
                re.IGNORECASE,
            ),
        },
        "north-america/canada/vancouver.htm": {
            "UUID": os.getenv("VANCOUVER_UUID"),
            "regex": re.compile(
                r"^(?P<temperature>\d+(\.\d+)?).C\s+",
                re.IGNORECASE,
            ),
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
