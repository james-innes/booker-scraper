# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os
import csv
import json
import time
import re
import mariadb
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
from items import BookerBarcodeItem

load_dotenv()

conn = mariadb.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
)

cur = conn.cursor(buffered=True)


class BookerBarcodes(CrawlSpider):
    name = 'booker_mb'
    allowed_domains = ['booker.co.uk']
    custom_settings = {"FEEDS": {"barcodes.csv": {"format": "csv"}}}
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

        cur.execute('SELECT sub_cat_code FROM sub_cat')

        for result in cur:
            yield Request(url=f'https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname={result[0]}', headers=headers, callback=self.parse_barcodes, cb_kwargs=dict(sub_cat_code=result[0]))

        cur.close()
        conn.close()

    def parse_barcodes(self, response, sub_cat_code):
        for product in response.xpath('//*[@class="genericListItem"]'):
            l = ItemLoader(item=BookerBarcodeItem(),
                           selector=product, response=response)
            l.add_xpath('barcode', 'td[1]//img/@alt')
            l.add_xpath('code', 'td[2]//text()')
            l.add_value('sub_cat_code', sub_cat_code)
            yield l.load_item()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BookerBarcodes)
    process.start()
