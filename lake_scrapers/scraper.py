from abc import abstractmethod
from dataclasses import dataclass


import bs4
import httpx
import lxml.etree

from lake_scrapers import LakeTemperatureItem


@dataclass
class Request:
    def __init__(self, path: str):
        self.path = path


class Scraper:
    base_url: str
    paths: list[str]
    headers: dict = None

    @staticmethod
    def soup(response: httpx.Response) -> bs4.BeautifulSoup:
        response.raise_for_status()

        return bs4.BeautifulSoup(response.text, 'html.parser')

    def request(self, path: str) -> httpx.Response:
        url = "/".join([self.base_url.rstrip("/"), path.lstrip("/")])

        return httpx.get(url, headers=self.headers, timeout=15, follow_redirects=True)

    @abstractmethod
    def parse(self, response: httpx.Response) -> LakeTemperatureItem: ...

    @staticmethod
    def xpath(xpath: str, response: httpx.Response, _type: str = "html"):
        if _type == "html":
            tree: lxml.etree.Element = lxml.etree.HTML(response.content)
        elif _type == "xml":
            tree: lxml.etree.Element = lxml.etree.XML(response.content)
        else:
            raise NotImplementedError(f"this only supports 'html' and 'xml' not {_type}")

        return tree.xpath(xpath)
