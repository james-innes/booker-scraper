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


class BookerBarcodeItem(scrapy.Item):
    Barcode = scrapy.Field()
    Product_Code = scrapy.Field()
    Product_Description = scrapy.Field()
    Pack_Size = scrapy.Field()
    Sell_Price = scrapy.Field()
    RRP = scrapy.Field()


class BookerProductItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    cat_id = scrapy.Field()
    sub_cat_id = scrapy.Field()
    shelf_id = scrapy.Field()
    wsp_exl_vat = scrapy.Field()
    wsp_inc_vat = scrapy.Field()
    rrp = scrapy.Field()
    por = scrapy.Field()
    vat = scrapy.Field()
    size = scrapy.Field()
    ws_qty = scrapy.Field()
    rt_qty = scrapy.Field()
    pack_type = scrapy.Field()
    img_small_guid = scrapy.Field()
    img_big_guid = scrapy.Field()
    brand = scrapy.Field()
    origin_country = scrapy.Field()
    packed_country = scrapy.Field()
    storage_type = scrapy.Field()
    beverage_type = scrapy.Field()
    alcohol_volume = scrapy.Field()
    alcohol_units = scrapy.Field()
    description = scrapy.Field()
    tasting_notes = scrapy.Field()
    allergy_advice = scrapy.Field()
    ingredients = scrapy.Field()
    nutrition = scrapy.Field()
    manufacturer = scrapy.Field()
    packaging = scrapy.Field()
