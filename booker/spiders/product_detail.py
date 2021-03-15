# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os
import csv
import re
from dotenv import load_dotenv
import sqlite3

import scrapy
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from booker.items import ProductDetail

load_dotenv()


class ProductDetailSpider(scrapy.Spider):
    name = 'product_detail'
    allowed_domains = ['booker.co.uk']
    start_urls = ['https://www.booker.co.uk']
    custom_settings = {"FEEDS": {"product_detail.csv": {"format": "csv"}}}

    def parse(self, response):
        for row in sqlite3.connect('stores.db').execute("SELECT * FROM product_list").fetchall():
            yield Request(
                url=f'https://www.booker.co.uk/products/product%20detail?Code={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION'), '.ASPXAUTH': os.getenv('ASPXAUTH'), 'BookerMessage': 'WebsiteBulletinCheckedDate=21%2f01%2f2021+18%3a47%3a01'}, callback=self.parse_product_detail, cb_kwargs=dict(code=row[0]))

    def parse_product_detail(self, response, code):
        description = "".join(response.css(
            '#product-details-show-more :not([id^=show-less])').extract())

        if response.css('#categories p').extract():
            catagories = "<h4>Categories</h4>" + \
                response.css('#categories p').extract()[0]
        else:
            catagories = ""

        infoSection = ""
        for card in response.css('.desplegabledesktop .product-cards .card'):
            header = "<h4>" + \
                card.css('.card-header h4::text').extract()[0] + "</h4>"
            body = card.css('.card-body').extract()[0]
            infoSection = infoSection + header + body

        info = description + catagories + "<div>" + infoSection + "</div>"

        l = ItemLoader(item=ProductDetail(), response=response)
        l.add_value('code', code)
        l.add_css('name', '.product-main > h4::text')
        l.add_css('img_big', '.product-image figure>img::attr(src)')
        l.add_value('info', info)

        yield l.load_item()
