import os

from lake_scrapers import convert_timestamp, LakeTemperatureItem
from lake_scrapers.scraper import Scraper


class PegelonlineScraper(Scraper):
    data = {
        "580412": {"UUID": os.getenv("POTSDAM_UUID")},
        "2730010": {"UUID": os.getenv("COLOGNE_UUID")},
        "9530020": {"UUID": os.getenv("HUSUM_UUID")},
    }
    base_url = "https://www.pegelonline.wsv.de"
    paths = [
        "gast/stammdaten?pegelnr=2730010",
        "gast/stammdaten?pegelnr=580412",
        "gast/stammdaten?pegelnr=9530020",
    ]

    def parse(self, response, **kwargs):
        temp_xpath = "//td[contains(text(), 'Wassertemperatur')]/../*[2]//text()"
        time_xpath = "//td[contains(text(), 'Wassertemperatur')]/../*[3]//text()"

        temperature = self.xpath(temp_xpath, response)
        temperature = temperature[0]
        timestamp = self.xpath(time_xpath, response)[0]
        timestamp = timestamp
        timestamp = convert_timestamp(timestamp)

        query = response.request.url.query.decode("UTF-8")
        pegelnr = query.rsplit("=")[-1]
        uuid = self.data[pegelnr]["UUID"]

        return LakeTemperatureItem(
            temperature=temperature, timestamp=timestamp, uuid=uuid
        )
