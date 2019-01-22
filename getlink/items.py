# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetlinkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #time = scrapy.Field()
    #readtimes = scrapy.Field()
    link = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    #***************************
    type = scrapy.Field()
    source = scrapy.Field()
    saveTime = scrapy.Field()
    pubTime = scrapy.Field()
    site = scrapy.Field()
    author = scrapy.Field()
