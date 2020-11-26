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

import pandas as pd
import numpy as np

load_dotenv()


class CodeSpider(CrawlSpider):
    name = 'booker_mb'
    allowed_domains = ['booker.co.uk']
    start_urls = ['https://www.booker.co.uk/home.aspx']

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        self.driver.get('https://www.booker.co.uk/home.aspx')
        self.driver.find_element_by_id ('OutsideHomePageControl_CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'))
        self.driver.find_element_by_id('OutsideHomePageControl_cmdCustomerNumber').click()
        time.sleep(0.5)

        self.driver.find_element_by_id('LoginControl_EmailSingle').send_keys(os.getenv('BOOKER_EMAIL'))
        self.driver.find_element_by_id('LoginControl_PasswordSingle').send_keys(os.getenv('BOOKER_PASSWORD'))
        self.driver.find_element_by_id('LoginControl_EnterEmailPasswordSubmit').click()

        # Gets the Selenium response and passes it onto Scrapy
        self.cookie = self.driver.get_cookie('ASP.NET_SessionId')
        self.parse(response=self.driver.page_source)
        self.driver.quit()

    def parse(self, response):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': f'ASP.NET_SessionId={self.cookie['value']}',
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

        for index, row in df.iterrows():
            yield Request(
                url=f'https://www.booker.co.uk/catalog/products.aspx?categoryName={row[0]}', headers=headers, callback=self.parse_product_list)

    def parse_product_list(self, response):
        for href in response.css('tr .info_r1 a::attr(href)').extract():
            print(parse_qs(urlparse(href).query)['code'][0])

        next_page_url = response.urljoin(response.xpath('//a[text()='Next >>']//@href').get())

        if next_page_url is not None:
            yield Request(next_page_url, callback=self.parse_product_list)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CodeSpider)
    process.start()
