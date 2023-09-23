import os
from datetime import datetime

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class CuxhavenScraper(Scraper):
    data = {"cuxhaven": {"UUID": os.getenv("CUXHAVEN_UUID")}}
    base_url = "https://www.tourlogger.de"
    paths = ["wassertemperatur/cuxhaven"]

    def parse(self, response, **kwargs):
        css_class = ".tourlogger-wassertemperatur"
        timestamp = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
        timestamp = convert_timestamp(timestamp, is_timestamp=True)
        soup = self.soup(response)

        temperature = soup.select_one(css_class).text
        path = response.request.url.path
        key = path.rsplit("/")[-2]
        uuid = self.data[key]["UUID"]

        return LakeTemperatureItem(
            temperature=temperature, timestamp=timestamp, uuid=uuid
        )
