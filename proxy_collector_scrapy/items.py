# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
    # define the fields for your item here like:
    host = scrapy.Field()
    port = scrapy.Field()
    _type = scrapy.Field()
    ping = scrapy.Field()
