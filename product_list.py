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
from items import BookerProductItem

load_dotenv()

conn = mariadb.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
)

cur = conn.cursor(buffered=True)


class BookerProductList(CrawlSpider):
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

        cur.execute('SELECT sub_cat_code FROM sub_cat')

        for result in cur:
            yield Request(
                url=f'https://www.booker.co.uk/catalog/products.aspx?categoryName={result[0]}', headers=headers, callback=self.parse_product_list)

        cur.close()
        conn.close()

    def parse_product_list(self, response):

        for href in response.css('tr .info_r1 a::attr(href)').extract():
            print(parse_qs(urlparse(href).query)['code'][0])

        for pr in response.xpath('.//*[@class="pr"]'):
            l = ItemLoader(item=BookerProductItem(), selector=pr, response=response)
            l.add_xpath('code', ".//td[@class='packm']/div/text()")
            l.add_css('name', '.info_r1 a::text')
            l.add_xpath('wsp_exl_vat', ".//li[@class='wsp']/text()")
            l.add_css('rrp', '.price ul li:contains(\"RRP\")::text')
            l.add_css('por', '.price ul li:contains(\"POR\")::text')
            l.add_css('vat', '.price ul li:contains(\"VAT\")::text')
            l.add_xpath('ws_qty', ".//div[@class='pibox']/descendant::*/text()")
            l.add_css('rt_qty', '.pisize::text')
            l.add_css('img_small_guid', 'img.pi::attr(src)')
            l.add_css('storage_type', 'td.icons li::text')
            yield l.load_item()

        next_page_url = response.urljoin(
            response.xpath('//a[text()="Next >> "]//@href').get())

        if next_page_url is not None:
            yield Request(next_page_url, callback=self.parse_product_list)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BookerProductList)
    process.start()
