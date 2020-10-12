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
    
class BookerBarcodeItem(scrapy.Item):
    Barcode = scrapy.Field()
    Product_Code = scrapy.Field()
    Product_Description = scrapy.Field()
    Pack_Size = scrapy.Field()
    Sell_Price = scrapy.Field()
    RRP = scrapy.Field()
