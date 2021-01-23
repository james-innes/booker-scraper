# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, re
from urllib.parse import urljoin, parse_qs, urlparse
from dotenv import load_dotenv
import sqlite3

import scrapy
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from booker.items import Barcode

load_dotenv()

class BarcodeSpider(scrapy.Spider):
	name = 'barcode'
	allowed_domains = ['booker.co.uk']
	start_urls = ['https://www.booker.co.uk']
	custom_settings = {"FEEDS": {"barcode.csv": {"format": "csv"}}}

	def parse(self, response):
		for row in sqlite3.connect('stores.db').execute("SELECT * FROM sitemap").fetchall():
			yield Request(url=f'https://www.booker.co.uk/products/print-product-list-ungroup?printType=ProductList&categoryName={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION'), '.ASPXAUTH': os.getenv('ASPXAUTH')}, callback=self.parse_barcode, cb_kwargs=dict(sub_cat_code=row[0]))

	def parse_barcode(self, response, sub_cat_code):
		for tr in response.css('.table-desktop tr'):
			l = ItemLoader(item=Barcode(), selector=tr, response=response)
			l.add_css('barcode', 'svg::attr(jsbarcode-value)')
			l.add_css('code', 'td:nth-of-type(2)::text')
			l.add_value('sub_cat_code', sub_cat_code)
			yield l.load_item()