# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, time, re
from urllib.parse import urljoin, parse_qs, urlparse
from dotenv import load_dotenv

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

class ProductSpider(CrawlSpider):
    name = 'booker_mb'
    allowed_domains = ['booker.co.uk']
    custom_settings = {"FEEDS": {"product_list.csv": {"format": "csv"}}}
    start_urls = ['https://www.booker.co.uk/home.aspx']

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        self.driver.get('https://www.booker.co.uk/home.aspx')
        self.driver.find_element_by_id(
            'OutsideHomePageControl_CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'))
        self.driver.find_element_by_id(
            'OutsideHomePageControl_cmdCustomerNumber').click()
        time.sleep(0.5)

        self.driver.find_element_by_id(
            'LoginControl_EmailSingle').send_keys(os.getenv('BOOKER_EMAIL'))
        self.driver.find_element_by_id('LoginControl_PasswordSingle').send_keys(
            os.getenv('BOOKER_PASSWORD'))
        self.driver.find_element_by_id(
            'LoginControl_EnterEmailPasswordSubmit').click()

        # Gets the Selenium response and passes it onto Scrapy
        self.cookie = self.driver.get_cookie('ASP.NET_SessionId')
        self.parse(response=self.driver.page_source)
        self.driver.quit()

    def parse(self, response):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': f'ASP.NET_SessionId={self.cookie["value"]}',
            'Host': 'www.booker.co.uk',
            'Referer': 'https://www.booker.co.uk/catalog/mybooker.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }

        df = pd.read_csv('sub_cat_code.csv')

        for index, result in df.iterrows():
            yield Request(
                url=f'https://www.booker.co.uk/catalog/products.aspx?categoryName={result[0]}', headers=headers, callback=self.parse_product_list, cb_kwargs=dict(sub_cat_code=result[0]))

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


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ProductSpider)
    process.start()
