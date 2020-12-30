# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, re
from urllib.parse import urljoin, parse_qs, urlparse
from dotenv import load_dotenv

import scrapy
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import HtmlResponse

import pandas as pd
import numpy as np

load_dotenv()

class CodeSpider(scrapy.Spider):
    name = 'code'
    allowed_domains = ['booker.co.uk']
    start_urls = ['https://www.booker.co.uk/home.aspx']

    def parse(self, response):
        df = pd.read_csv('sub_cat_code.csv')

        for index, row in df.iterrows():
            yield Request(
                url=f'https://www.booker.co.uk/catalog/products.aspx?categoryName={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION')}, callback=self.parse_code)

    def parse_code(self, response):
        for href in response.css('tr .info_r1 a::attr(href)').extract():
            print(parse_qs(urlparse(href).query)['code'][0])

        next_page_url = response.urljoin(response.xpath('//a[text()="Next >>"]//@href').get())

        if next_page_url is not None:
            yield Request(next_page_url, callback=self.parse_product_list)
