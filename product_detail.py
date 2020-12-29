# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, time, re
from urllib.parse import urljoin, parse_qs, urlparse
from dotenv import load_dotenv
import lxml.html.clean as clean
import w3lib.html

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from items import Product

import pandas as pd
import numpy as np


load_dotenv()

safe_attrs = clean.defs.safe_attrs
cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())

class ProductSpider(CrawlSpider):
    name = 'booker_mb'
    allowed_domains = ['booker.co.uk']
    start_urls = ['https://www.booker.co.uk/home.aspx']
    custom_settings = {"FEEDS": {"product_detail.csv": {"format": "csv"}}}

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        self.driver.get('https://www.booker.co.uk/home.aspx')
        self.driver.find_element_by_id('OutsideHomePageControl_CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'))
        self.driver.find_element_by_id('OutsideHomePageControl_cmdCustomerNumber').click()
        time.sleep(0.5)

        self.driver.find_element_by_id('LoginControl_EmailSingle').send_keys(os.getenv('BOOKER_EMAIL'))
        self.driver.find_element_by_id('LoginControl_PasswordSingle').send_keys(os.getenv('BOOKER_PASSWORD'))
        self.driver.find_element_by_id('LoginControl_EnterEmailPasswordSubmit').click()

        self.cookie = self.driver.get_cookie('ASP.NET_SessionId')
        self.parse(response=self.driver.page_source)
        self.driver.quit()

    def parse(self, response):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': f"ASP.NET_SessionId={self.cookie['value']}",
            'Host': 'www.booker.co.uk',
            'Referer': 'https://www.booker.co.uk/catalog/mybooker.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }

        codes = [
            [258721],
            [173128],
            [255483],
        ]

        df = pd.read_csv('code.csv')

        for index, row in df.iterrows():
            yield Request(
                url=f'https://www.booker.co.uk/catalog/productinformation.aspx?code={row[0]}', headers=self.headers, callback=self.parse_product_detail, cb_kwargs=dict(code=row[0]))


    def parse_product_detail(self, response, code):

        nutritionTableRaw = response.css('h1:contains("Nutrition") + div table').extract_first()

        if nutritionTableRaw is None:
            nutritionTable = None
        else:
            nutritionTable = cleaner.clean_html(w3lib.html.replace_escape_chars(nutritionTableRaw, which_ones=('\n', '\t', '\r'), encoding=None))

     
        l = ItemLoader(item=Product(), response=response)
        l.add_css('code', ".pip .pir ul li:contains('Code: ') span::text")
        l.add_css('name', '.pip h3::text')
        l.add_css('cat_code', '.siteNav dt.selected::attr(cat)')
        l.add_css('cat_name', '.siteNav dt.selected::text')
        l.add_css('sub_cat_code', '.siteNav dt.selected + dd li.selected::attr(cat)')
        l.add_css('sub_cat_name', '.siteNav dt.selected + dd li.selected::text')

        l.add_css('wsp_exl_vat', ".pip .pir ul li:contains('WSP: ') span::text")
        l.add_css('wsp_inc_vat', ".pip .pir ul li:contains('WSP inc VAT: ') span::text")
        l.add_css('rrp', ".pip .pir ul li:contains('RRP: ') span::text")
        l.add_css('por', ".pip .pir ul li:contains('POR: ') span::text")
        l.add_css('vat', ".pip .pir ul li:contains('VAT: ') span::text")
        l.add_css('size', ".pip .pir ul li:contains('Size: ') span::text")

        l.add_css('pack_type', 'a[href*="By+Pack+Type"]::text')
        l.add_css('unit_description', '.pip .pir ul li:contains("Unit Description: ") span::text')
        l.add_css('additives', 'a[href*="By+Additives"]::text')
        l.add_css('img_small_url', '.pir .piTopInfo img::attr(src)')

        l.add_css('brand', '.pip #catLinks b:contains("By Brand:") + span a::text')

        l.add_css('origin_country', 'a[href*="By+Country+of+Origin"]::text')
        l.add_css('packed_country', 'a[href*="By+Packed+In"]::text')
        l.add_css('storage_type', 'a[href*="By+Storage+Type"]::text')
        l.add_css('beverage_type', 'a[href*="By+Beverage+Type"]::text')
        l.add_css('alcohol_volume', '.pip .pir ul li:contains("Alcohol by Volume: ") span::text')
        l.add_css('alcohol_units', '.pip .pir ul li:contains("Alcohol Units: ") span::text')

        l.add_css('description', 'h1:contains("Description") + p')
        l.add_css('allergy_advice', 'h1:contains("Allergy Advice") + ul li')
        l.add_css('ingredients', 'h1:contains("Ingredients") + ul li')

        l.add_value('nutrition_table', nutritionTable)
        l.add_css('nutrition_notes', 'h1:contains("Nutrition") + div + p')

        l.add_css('manufacturer', 'h1:contains("Manufacturer") + p::text')
        l.add_css('packaging', 'h1:contains("Packaging") + ul li::text')
        l.add_css('prepare_and_use', 'h1:contains("Prepare and Use") + p::text')
        l.add_css('storage_information','h1:contains("Storage Information") + ul li::text')
        l.add_css('freezing_guidelines','h1:contains("Freezing Guidelines") + ul li::text')
        l.add_css('additional_information', 'h1:contains("Additional Information") + p::text')
        l.add_css('recycling', 'h1:contains("Recycling") + ul li::text')
        l.add_css('tasting_notes', 'h1:contains("Tasting Notes") + p::text')

        l.add_css('current_vintage', 'a[href*="By+Current+Vintage"]::text')
        l.add_css('wine_colour', 'a[href*="By+Wine+Colour"]::text')
        l.add_css('producer', 'a[href*="By+Producer"]::text')
        l.add_css('grape_variety', 'a[href*="By+Grape+Variety"]::text')
        l.add_css('closure_type', 'a[href*="By+Type+of+Closure"]::text')
        l.add_css('wine_maker', 'a[href*="By+Wine+Maker"]::text')

        l.add_css('case_of', 'a[href*="Case"]::text',)

        request = Request(url=f"https://www.booker.co.uk/catalog/displayimage.aspx?vid={code}", headers=self.headers, callback=self.parse_image)
        request.meta['l'] = l

        yield request

    def parse_image(self, response):
        imgUrlBig = 'https://www.booker.co.uk' + response.css('img::attr(src)').extract_first()
        l = response.meta['l']
        l.add_value('img_big_url', imgUrlBig)
        yield l.load_item()

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ProductSpider)
    process.start()