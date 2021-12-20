import inspect
import logging
import os
import sys
from typing import Tuple, Optional

import requests
import urllib3


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.Logger(name)
    ch = logging.StreamHandler(sys.stdout)

    formatting = "[{}] %(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s#%(lineno)d | %(message)s".format(name)
    formatter = logging.Formatter(formatting)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.setLevel(level)

    return logger


def send_data_to_backend(water_information: Tuple[str, float], uuid: str) -> Tuple[Optional[requests.Response], str]:
    BACKEND_URL = os.getenv("BACKEND_URL") or "http://backend:8080"
    BACKEND_PATH = os.getenv("BACKEND_PATH") or "lake/{}/temperature"
    API_KEY = os.getenv("API_KEY")

    logger = create_logger(inspect.currentframe().f_code.co_name)
    path = BACKEND_PATH.format(uuid)
    url = "/".join([BACKEND_URL, path])

    water_timestamp, water_temperature = water_information
    if water_temperature <= 0:
        return None, "water_temperature is <= 0, please approve this manually."

    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"temperature": water_temperature, "time": water_timestamp}
    logger.debug(f"Send {data} to {url}")

    try:
        response = requests.put(url, json=data, headers=headers)
        logger.debug(f"success: {response.ok} | content: {response.content}")
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError):
        logger.exception(f"Error while connecting to backend ({url})", exc_info=True)
        return None, url

    return response, url
