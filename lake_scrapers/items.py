# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LakeTemperatureItem(scrapy.Item):
    temperature = scrapy.Field()
    timestamp = scrapy.Field()
    uuid = scrapy.Field()


class LakeScrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
