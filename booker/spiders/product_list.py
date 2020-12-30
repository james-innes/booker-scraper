# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, re
from urllib.parse import urljoin
from dotenv import load_dotenv

import scrapy
from scrapy.http import Request    
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from booker.items  import Product

import pandas as pd
import numpy as np

load_dotenv()

class ProductListSpider(scrapy.Spider):
    name = 'product_list'
    allowed_domains = ['booker.co.uk']
    custom_settings = {"FEEDS": {"product_list.csv": {"format": "csv"}}}
    start_urls = ['https://www.booker.co.uk/home.aspx']

    def parse(self, response):
        df = pd.read_csv('sub_cat_code.csv')

        for index, result in df.iterrows():
            yield Request(
                url=f'https://www.booker.co.uk/catalog/products.aspx?categoryName={result[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION')}, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_code=result[0]))

    def parse_product_list(self, response, sub_cat_code):
        for pr in response.xpath('.//*[@class="pr"]'):
            l = ItemLoader(item=Product(),
                           selector=pr, response=response)
            l.add_css('code', ".packm div::text")
            l.add_css('name', '.info_r1 a::text')
            l.add_xpath('wsp_exl_vat', ".//li[@class='wsp']/text()")
            l.add_css('rrp', '.price ul li:contains(\"RRP\")::text')
            l.add_css('por', '.price ul li:contains(\"POR\")::text')
            l.add_css('vat', '.price ul li:contains(\"VAT\")::text')
            l.add_xpath('ws_qty', ".//div[@class='pibox']/descendant::*/text()")
            l.add_css('rt_qty', '.pisize::text')
            l.add_value('img_small_url', 'https://www.booker.co.uk' + response.css('img.pi::attr(src)'))
            l.add_css('storage_type', 'td.icons li::text')
            l.add_value('sub_cat_code', sub_cat_code)
            yield l.load_item()

        next_page_url = response.xpath('//a[text()="Next >>"]//@href').get()
        absolute_next_page_url = response.urljoin(next_page_url)
        if next_page_url is not None:
            yield Request(absolute_next_page_url, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_code=sub_cat_code))