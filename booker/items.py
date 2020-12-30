# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import replace_escape_chars

class Sitemap(scrapy.Item):
    sub_cat_code = scrapy.Field()
    cat_name = scrapy.Field()
    sub_cat_name = scrapy.Field()

class Category(scrapy.Item):
    code = scrapy.Field()
    sub_cat_name = scrapy.Field()
    sub_cat_code = scrapy.Field()

class Product(scrapy.Item):
    default_output_processor = TakeFirst()
    
    code = scrapy.Field()
    name = scrapy.Field()
    img_small = scrapy.Field()
    img_big = scrapy.Field()

    wsp_exl_vat = scrapy.Field()
    wsp_inc_vat = scrapy.Field()
    rrp = scrapy.Field()
    por = scrapy.Field()
    vat = scrapy.Field()
    size = scrapy.Field()
    unit_description = scrapy.Field()

    brand = scrapy.Field()
    pack_type = scrapy.Field()
    on_offer = scrapy.Field()
    additives = scrapy.Field()
    origin_country = scrapy.Field()
    packed_country = scrapy.Field()
    storage_type = scrapy.Field()
    beverage_type = scrapy.Field()
    alcohol_volume = scrapy.Field()
    alcohol_units = scrapy.Field()
    current_vintage = scrapy.Field()
    wine_colour = scrapy.Field()
    producer = scrapy.Field()
    grape_variety = scrapy.Field()
    closure_type = scrapy.Field()
    wine_maker = scrapy.Field()
    case_of = scrapy.Field()

    product_info = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars),
        output_processor=Join(),
    )

class Barcode(scrapy.Item):
    barcode = scrapy.Field()
    code = scrapy.Field()
    sub_cat_code = scrapy.Field()