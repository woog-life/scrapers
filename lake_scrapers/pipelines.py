# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

import pytz

from lake_scrapers import send_data_to_backend


def convert_timestamp(timestamp, time_format="%d.%m.%Y %H:%M Uhr", is_timestamp=False, is_timestamp_nanosecond=False,
                      timezone="Europe/Berlin") -> str:
    if not (is_timestamp or is_timestamp_nanosecond):
        time = datetime.strptime(timestamp, time_format)
    elif is_timestamp_nanosecond:
        time = datetime.fromtimestamp(int(timestamp) / 1000)
    else:
        time = datetime.fromtimestamp(int(timestamp))

    local = pytz.timezone(timezone)
    time = local.localize(time)
    return time.astimezone(pytz.utc).isoformat()


class LakeScrapersPipeline:
    def process_item(self, item, _spider):
        temperature = float(item['temperature'].replace(",", "."))
        timestamp = item['timestamp']
        send_data_to_backend((timestamp, temperature), item['uuid'])

        return item
