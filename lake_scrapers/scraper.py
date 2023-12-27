import urllib.robotparser
from abc import abstractmethod
from dataclasses import dataclass

import bs4
import httpx
import lxml.etree

from lake_scrapers import LakeTemperatureItem, create_logger


@dataclass
class Request:
    def __init__(self, path: str):
        self.path = path


class Scraper:
    base_url: str
    paths: list[str]
    headers: dict = {"User-Agent": "woog.life-scraper"}

    def __init__(self):
        logger = create_logger("scraper.__init__")
        robots_url = self.base_url.rstrip("/") + "/robots.txt"
        self.robots = urllib.robotparser.RobotFileParser()
        try:
            response = httpx.get(
                robots_url, follow_redirects=True, timeout=15, headers=self.headers
            )
        except httpx.HTTPError as e:
            logger.error(
                f"got http error ({e}) when trying to retrieve robots.txt from {robots_url}"
            )
            logger.error("setting `disallow_all = True` for this robot")
            self.robots.disallow_all = True
        except httpx.ReadTimeout:
            logger.error(f"got read timeout error for {robots_url}")
            logger.error("setting `disallow_all = True` for this scraper")
            self.robots.disallow_all = True
        else:
            self.robots.parse(response.text.splitlines())

    @staticmethod
    def soup(response: httpx.Response) -> bs4.BeautifulSoup:
        response.raise_for_status()

        return bs4.BeautifulSoup(response.text, "html.parser")

    def request(self, path: str, retry_count: int = 0) -> httpx.Response:
        logger = create_logger("scraper.request")
        url = "/".join([self.base_url.rstrip("/"), path.lstrip("/")])

        # noinspection PyBroadException
        try:
            return httpx.get(
                url, headers=self.headers, timeout=15, follow_redirects=True
            )
        except Exception as e:
            logger.error(f"retry count: {retry_count}", exc_info=True)
            if retry_count == 0:
                raise e

        return self.request(path, retry_count=retry_count - 1)

    @abstractmethod
    def parse(self, response: httpx.Response) -> LakeTemperatureItem:
        raise NotImplementedError

    @staticmethod
    def xpath(xpath: str, response: httpx.Response, _type: str = "html"):
        if _type == "html":
            tree: lxml.etree.Element = lxml.etree.HTML(response.content)
        elif _type == "xml":
            tree: lxml.etree.Element = lxml.etree.XML(response.content)
        else:
            raise NotImplementedError(
                f"this only supports 'html' and 'xml' not {_type}"
            )

        return tree.xpath(xpath)

    def is_allowed_to_scrape(self, path: str):
        user_agent = self.headers.get("User-Agent", "")
        return self.robots.can_fetch(user_agent, path)
