# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

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


class Barcode(scrapy.Item):
    barcode = scrapy.Field()
    code = scrapy.Field()
    sub_cat_code = scrapy.Field()


class Product(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    cat_code = scrapy.Field()
    cat_name = scrapy.Field()
    sub_cat_code = scrapy.Field()
    sub_cat_name = scrapy.Field()
    wsp_exl_vat = scrapy.Field()
    wsp_inc_vat = scrapy.Field()
    rrp = scrapy.Field()
    por = scrapy.Field()
    vat = scrapy.Field()
    size = scrapy.Field()
    ws_qty = scrapy.Field()
    rt_qty = scrapy.Field()
    pack_type = scrapy.Field()
    unit_description = scrapy.Field()
    on_offer = scrapy.Field()
    additives = scrapy.Field()
    img_small = scrapy.Field()
    img_big = scrapy.Field()
    brand = scrapy.Field()
    origin_country = scrapy.Field()
    packed_country = scrapy.Field()
    storage_type = scrapy.Field()
    beverage_type = scrapy.Field()
    alcohol_volume = scrapy.Field()
    alcohol_units = scrapy.Field()
    description = scrapy.Field()
    allergy_advice = scrapy.Field()
    ingredients = scrapy.Field()
    nutrition_table = scrapy.Field()
    nutrition_notes = scrapy.Field()
    manufacturer = scrapy.Field()
    packaging = scrapy.Field()
    alternative_products = scrapy.Field()
    prepare_and_use = scrapy.Field()
    storage_information = scrapy.Field()
    freezing_guidelines = scrapy.Field()
    additional_information = scrapy.Field()
    recycling = scrapy.Field()
    tasting_notes = scrapy.Field()
    current_vintage = scrapy.Field()
    wine_colour = scrapy.Field()
    producer = scrapy.Field()
    grape_variety = scrapy.Field()
    closure_type = scrapy.Field()
    wine_maker = scrapy.Field()
    case_of = scrapy.Field()

