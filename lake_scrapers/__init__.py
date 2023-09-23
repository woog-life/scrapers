import inspect
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Optional

import httpx
import pytz


@dataclass
class LakeTemperatureItem:
    temperature: str
    timestamp: str
    uuid: str


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.Logger(name)
    ch = logging.StreamHandler(sys.stdout)

    formatting = "[{}] %(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s#%(lineno)d | %(message)s".format(
        name
    )
    formatter = logging.Formatter(formatting)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.setLevel(level)

    return logger


def send_data_to_backend(
    water_information: Tuple[str, float], uuid: str
) -> Tuple[Optional[httpx.Response], str]:
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
        response = httpx.put(
            url, json=data, headers=headers, timeout=10, follow_redirects=True
        )
        logger.debug(
            f"success: {response.status_code < 400} | content: {response.content}"
        )
    except httpx.HTTPError:
        logger.exception(f"Error while connecting to backend ({url})", exc_info=True)
        return None, url

    return response, url


def convert_timestamp(
    timestamp,
    time_format="%d.%m.%Y %H:%M Uhr",
    is_timestamp=False,
    is_timestamp_nanosecond=False,
    timezone="Europe/Berlin",
) -> str:
    if not (is_timestamp or is_timestamp_nanosecond):
        time = datetime.strptime(timestamp, time_format)
    elif is_timestamp_nanosecond:
        time = datetime.fromtimestamp(int(timestamp) / 1000)
    else:
        time = datetime.fromtimestamp(int(timestamp))

    local = pytz.timezone(timezone)
    time = local.localize(time)
    return time.astimezone(pytz.utc).isoformat()
