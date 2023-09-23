import os
import re
from datetime import datetime

import httpx

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class BlaarmeersenScraper(Scraper):
    base_url = "https://bcam.farys.be"
    paths = [""]

    def parse(self, response: httpx.Response, **kwargs):
        temperature_regex = re.compile(r"Watertemperatuur\s*\n?\s*(\d+\.\d+)&#8451;", re.IGNORECASE)
        timestamp = datetime.now().timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)

        temperature = temperature_regex.findall(response.text)[0]

        uuid = os.getenv("BLAARMEERSEN_UUID")
        return LakeTemperatureItem(temperature=temperature, timestamp=timestamp, uuid=uuid)
