# -*- coding: utf-8 -*-
import scrapy


class PicsearchItem(scrapy.Item):
    """
    Describes picture item
    """
    url = scrapy.Field()
    source = scrapy.Field()
    number = scrapy.Field()
    image_source = scrapy.Field()
