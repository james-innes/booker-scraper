# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os
import csv
import json
import time
import re

from urllib.parse import urljoin
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from scrapy.http import FormRequest
from scrapy.settings import Settings
from scrapy.shell import inspect_response
from scrapy import Selector
from scrapy.http import HtmlResponse

load_dotenv()

class BookerProductList(CrawlSpider):
    header = {"User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/33.0"}
    name = "booker_mb"
    allowed_domains = ["booker.co.uk"]
    start_urls = [
        'https://www.booker.co.uk/account/loginregister/UserLogin.aspx']

    def __init__(self):
        # Use  Selenium to log in and get a response for Scrapy
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        self.driver.get(
            "https://www.booker.co.uk/account/loginregister/UserLogin.aspx")
        self.driver.find_element_by_id("LoginControl_CustomerNumberSingle").send_keys(
            os.getenv("BOOKER_ACCOUNT"))
        self.driver.find_element_by_id(
            "LoginControl_EnterCustomerNumberSubmit").click()
        time.sleep(0.5)

        self.driver.find_element_by_id(
            'LoginControl_EmailSingle').send_keys(os.getenv('BOOKER_EMAIL'))
        self.driver.find_element_by_id('LoginControl_PasswordSingle').send_keys(
            os.getenv('BOOKER_PASSWORD'))
        self.driver.find_element_by_id(
            'LoginControl_EnterEmailPasswordSubmit').click()

        # Gets the Selenium response and passes it onto Scrapy
        self.cookie = self.driver.get_cookie("ASP.NET_SessionId")
        self.parse(response=self.driver.page_source)
        self.driver.quit()

    def parse(self, response):
        headers = {
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

        with open('sitemap.json') as sitemap:
            for cat in json.load(sitemap)['categories']:
                for subCat in cat['subCategories']:
                    yield FormRequest(
                        url=f"https://www.booker.co.uk/catalog/products.aspx?categoryName={subCat['code']}", headers=headers, callback=self.getProductList, meta={'cat': cat, 'subCat': subCat})

    def getProductList(self, response):
        productLinks = response.css("tr .info_r1 a::attr(href)").extract()
        for productLink in productLinks:
            print({
                'catName': response.meta['cat']['name'],
                'subCatCode': response.meta['subCat']['code'],
                'url': productLink
            })


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BookerProductList)
    process.start()
