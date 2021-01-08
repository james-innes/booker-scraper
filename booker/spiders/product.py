# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, re
from dotenv import load_dotenv
import sqlite3

import scrapy
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from booker.items import Product

load_dotenv()

class ProductSpider(scrapy.Spider):
	name = 'product'
	allowed_domains = ['booker.co.uk']
	start_urls = ['https://www.booker.co.uk/home.aspx']
	custom_settings = {"FEEDS": {"product.csv": {"format": "csv"}}}

	def parse(self, response):			
		for row in sqlite3.connect('stores.db').execute("SELECT * FROM category").fetchall():
			yield Request(
				url=f'https://www.booker.co.uk/catalog/productinformation.aspx?code={row[0]}', cookies={'ASP.NET_SessionId': os.getenv('ASP_NET_SESSION')}, callback=self.parse_product_detail, cb_kwargs=dict(code=row[0]))


	def parse_product_detail(self, response, code):     
		l = ItemLoader(item=Product(), response=response)
		l.add_value('code', code)
		l.add_css('name', '.pip h3::text')
		l.add_css('img_small', ".pip .piTopInfo>div>div>a>img::attr(src)")

		l.add_css('wsp_exl_vat', ".pip .pir ul li:contains('WSP: ') span::text")
		l.add_css('wsp_inc_vat', ".pip .pir ul li:contains('WSP inc VAT: ') span::text")
		l.add_css('rrp', ".pip .pir ul li:contains('RRP: ') span::text")
		l.add_css('por', ".pip .pir ul li:contains('POR: ') span::text")
		l.add_css('vat', ".pip .pir ul li:contains('VAT: '):not(:first-child) span::text")
		l.add_css('size', ".pip .pir ul li:contains('Size: ') span::text")
		l.add_css('unit_description', '.pip .pir ul li:contains("Unit Description: ") span::text')

		l.add_css('brand', '.pip #catLinks b:contains("By Brand:") + span a::text')
		l.add_css('pack_type', 'a[href*="By+Pack+Type"]::text')
		l.add_css('additives', 'a[href*="By+Additives"]::text')
		l.add_css('origin_country', 'a[href*="By+Country+of+Origin"]::text')
		l.add_css('packed_country', 'a[href*="By+Packed+In"]::text')
		l.add_css('storage_type', 'a[href*="By+Storage+Type"]::text')
		l.add_css('beverage_type', 'a[href*="By+Beverage+Type"]::text')
		l.add_css('alcohol_volume', '.pip .pir ul li:contains("Alcohol by Volume: ") span::text')
		l.add_css('alcohol_units', '.pip .pir ul li:contains("Alcohol Units: ") span::text')
		l.add_css('current_vintage', 'a[href*="By+Current+Vintage"]::text')
		l.add_css('wine_colour', 'a[href*="By+Wine+Colour"]::text')
		l.add_css('producer', 'a[href*="By+Producer"]::text')
		l.add_css('grape_variety', 'a[href*="By+Grape+Variety"]::text')
		l.add_css('closure_type', 'a[href*="By+Type+of+Closure"]::text')
		l.add_css('wine_maker', 'a[href*="By+Wine+Maker"]::text')
		l.add_css('case_of', 'a[href*="Case"]::text',)

		l.add_css('product_info', ".pip .piSection:not(:first-child)")

		request = Request(url=f"https://www.booker.co.uk/catalog/displayimage.aspx?vid={code}", callback=self.parse_image)
		request.meta['l'] = l

		yield request

	def parse_image(self, response):
		l = response.meta['l']
		image = response.css("form img[id='imgImage']::attr(src)").extract()
		l.add_value('img_big', image)
		yield l.load_item()