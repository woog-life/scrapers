# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

import pytz

from lake_scrapers import send_data_to_backend


def convert_timestamp(timestamp, time_format="%d.%m.%Y %H:%M Uhr", timezone="Europe/Berlin") -> str:
    time = datetime.strptime(timestamp, time_format)
    local = pytz.timezone(timezone)
    time = local.localize(time)
    return time.astimezone(pytz.utc).isoformat()


class LakeScrapersPipeline:
    def process_item(self, item, _spider):
        temperature = float(item['temperature'].replace(",", "."))
        timestamp = convert_timestamp(item['timestamp'])
        send_data_to_backend((timestamp, temperature), item['uuid'])

        return item
