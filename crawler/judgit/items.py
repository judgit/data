# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JudgitItem(scrapy.Item):
    ministry = scrapy.Field()
    project_number1 = scrapy.Field()
    project_number2 = scrapy.Field()
    project_number3 = scrapy.Field()
    project_name = scrapy.Field()
    url = scrapy.Field()
    year = scrapy.Field()
