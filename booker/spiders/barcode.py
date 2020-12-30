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
from scrapy.loader import ItemLoader
from booker.items import Barcode

import pandas as pd
import numpy as np

load_dotenv()

class BarcodeSpider(scrapy.Spider):
	name = 'barcode'
	allowed_domains = ['booker.co.uk']
	custom_settings = {"FEEDS": {"barcode.csv": {"format": "csv"}}}
	start_urls = ['https://www.booker.co.uk/home.aspx']

	def parse(self, response):
		df = pd.read_csv('sitemap.csv')

		for index, row in df.iterrows():
			yield Request(url=f'https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION')}, callback=self.parse_barcode, cb_kwargs=dict(sub_cat_code=row[0]))

	def parse_barcode(self, response, sub_cat_code):
		for product in response.xpath('//*[@class="genericListItem"]'):
				l = ItemLoader(item=Barcode(), selector=product, response=response)
				l.add_xpath('barcode', 'td[1]//img/@alt')
				l.add_xpath('code', 'td[2]//text()')
				l.add_value('sub_cat_code', sub_cat_code)
				yield l.load_item()