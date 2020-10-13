# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, json, time, re, mariadb
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

# conn = mariadb.connect(
#     host=os.getenv('DB_HOST'),
#     user=os.getenv('DB_USER'),
#     password=os.getenv('DB_PASS'),
#     database=os.getenv('DB_NAME')
# )

# cur = conn.cursor(buffered=True)

class BookerProductDetail(CrawlSpider):
    name = 'booker_mb'
    allowed_domains = ['booker.co.uk']
    custom_settings = {'FEEDS': {'/data/product_detail.csv':{'format':'csv'}}}
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
        

        # cur.execute('SELECT code FROM product')

        # Mock response from db
        cur = [
            [258721],
            [173128],
            [255483],
        ]

        for result in cur:
            yield Request(
                url=f'https://www.booker.co.uk/catalog/productinformation.aspx?code={result[0]}', headers=headers, callback=self.parse_product_detail)

        # cur.close()
        # conn.close()

    def parse_product_detail(self, response):
    
        # Get Big image from Popup
        picturePopup = 'https://www.booker.co.uk' + response.css('.pip a::attr(href)').split("'")[1]
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(picturePopup)
        imgUrlBig = response.css('img::attr(src)').get_attribute('src').split("'")[0]
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        # End

        # Add topInfo dict to ItemLoader
        topInfo = dict([
            (
                i.split(':', 1)[0], i.split(':', 1)[1].strip(' %£')
            ) for i in response.css('.pir').text.split('\n')[:-2]
        ])

        wsQuantity, retailSize = topInfo['Size'].split(' x ')

        # Add these to ItemLoader
        'imgUrlBig': imgUrlBig,
        'imgUrlSmall': response.css('.pir .piTopInfo img::attr(src)').split("'")[0],
        'shelfCode': [int(s) for s in re.findall(r'\d\d\d\d\d\d', response.request.url)][1],
        'retailSize': retailSize,
        'wsQuantity': wsQuantity

        # Explore difference between xpath and css selector

        l = ItemLoader(item=BookerProductItem(), response=response)
        l.add_css('code', '.pip .pir ul li:contains(Code: ) span')
        l.add_css('name', '.pir h3::text()')
        l.add_css('cat_id', 'selector')
        l.add_css('sub_cat_id ', 'selector')
        l.add_css('shelf_id ', 'selector')
        l.add_css('wsp_exl_vat', 'selector')
        l.add_css('wsp_inc_vat', 'selector')
        l.add_css('rrp', 'selector')
        l.add_css('por', 'selector')
        l.add_css('vat', 'selector')
        l.add_css('size', 'selector')
        l.add_css('ws_qty', 'selector')
        l.add_css('rt_qty', 'selector')
        l.add_css('pack_type', 'selector')
        l.add_css('unit_description', 'selector')
        l.add_css('on_offer', 'selector')
        l.add_css('additives', 'selector')
        l.add_css('img_small_guid', 'selector')
        l.add_css('img_big_guid', 'selector')
        l.add_css('brand', 'selector')
        l.add_css('origin_country', 'selector')
        l.add_css('packed_country', 'selector')
        l.add_css('storage_type', 'selector')
        l.add_css('beverage_type', 'selector')
        l.add_css('alcohol_volume', 'selector')
        l.add_css('alcohol_units', 'selector')
        # Get below descriptive statements as dict maybe
        l.add_css('description', 'selector')
        l.add_css('allergy_advice', 'selector')
        l.add_css('ingredients', 'selector')
        # Work out how to save unpredictable table - maybe as html string
        l.add_css('nutrition', 'selector')
        l.add_css('manufacturer', 'selector')
        l.add_css('packaging', 'selector')
        l.add_css('alternative_products', 'selector')
        l.add_css('prepare_and_use', 'selector')
        l.add_css('storage_information', 'selector')
        l.add_css('freezing_guidelines', 'selector')
        l.add_css('additional_information', 'selector')
        l.add_css('recycling', 'selector')
        l.add_css('tasting_notes', 'selector')
        l.add_css('current_vintage', 'selector')
        l.add_css('wine_colour', 'selector')
        l.add_css('producer', 'selector')
        l.add_css('grape_variety', 'selector')
        l.add_css('closure_type', 'selector')
        l.add_css('wine_maker', 'selector')

        yield l.load_item()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BookerProductDetail)
    process.start()



