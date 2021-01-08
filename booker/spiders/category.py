# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, re
from urllib.parse import urljoin
from dotenv import load_dotenv
import sqlite3

import scrapy
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from booker.items import Product

load_dotenv()

class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['booker.co.uk']
    custom_settings = {"FEEDS": {"category.csv": {"format": "csv"}}}
    start_urls = ['https://www.booker.co.uk/home.aspx']

    def parse(self, response):
        for row in sqlite3.connect('stores.db').execute("SELECT * FROM sitemap").fetchall():
            yield Request(
                url=f'https://www.booker.co.uk/catalog/products.aspx?categoryName={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION')}, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_name=row[2], sub_cat_code=row[0]))

    def parse_product_list(self, response, sub_cat_name, sub_cat_code):
        for pr in response.xpath('.//*[@class="pr"]'):
            l = ItemLoader(item=Product(), selector=pr, response=response)
            l.add_css('code', ".packm div::text")
            l.add_value('sub_cat_name', sub_cat_name)
            l.add_value('sub_cat_code', sub_cat_code)
            yield l.load_item()

        next_page_url = response.urljoin(
            response.xpath('//a[text()="Next >>"]//@href').get())

        if next_page_url is not None:
            yield Request(next_page_url, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_name=sub_cat_name, sub_cat_code=sub_cat_code))
