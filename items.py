# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


import scrapy


class BookerMbItem(scrapy.Item):
    BPLIC = scrapy.Field()
    alt = scrapy.Field()
    pack = scrapy.Field()
    info_r1 = scrapy.Field()
    info_r2 = scrapy.Field()
    promotionText = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
