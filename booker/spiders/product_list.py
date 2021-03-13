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
from booker.items import ProductList

load_dotenv()

class ProductListSpider(scrapy.Spider):
	name = 'product_list'
	allowed_domains = ['booker.co.uk']
	start_urls = ['https://www.booker.co.uk']
	custom_settings = {"FEEDS": {"product_list.csv": {"format": "csv"}}}

	def parse(self, response):
		for row in sqlite3.connect('stores.db').execute("SELECT * FROM sitemap").fetchall():
		# for row in [["CS13_201500", "Non-Food", "Crockery and Tableware"]]:
			yield Request(
				url=f'https://www.booker.co.uk/products/product-list?categoryName={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION'), '.ASPXAUTH': os.getenv('ASPXAUTH'), 'BookerMessage': 'WebsiteBulletinCheckedDate=21%2f01%2f2021+18%3a47%3a01'}, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_name=row[2], sub_cat_code=row[0]))

	def parse_product_list(self, response, sub_cat_name, sub_cat_code):
		for row in response.css('.rowUnGrouped .product-model'):
			l = ItemLoader(item=ProductList(), selector=row, response=response)
			code = row.css('.product-code::text').extract()[0].strip()
			l.add_value('code', code)
			l.add_value('sub_cat_code', sub_cat_code)
			l.add_css('img_small', '.product-image img::attr(src)')
			l.add_css('wsp_inc_vat', '.price p::text')
			l.add_css('rrp', 'span:contains("RRP: ")::text')
			l.add_css('por', 'span:contains("POR: ")::text')

			yield l.load_item()

		next_page_url = response.urljoin(
			response.css('.page-link[rel=next]::attr(href)').get())

		if next_page_url is not None:
			yield Request(next_page_url, cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION'), '.ASPXAUTH': os.getenv('ASPXAUTH')}, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_name=sub_cat_name, sub_cat_code=sub_cat_code))
