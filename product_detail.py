# -*- coding: utf-8 -*-
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, csv, json, time, re, mariadb
from urllib.parse import urljoin, parse_qs, urlparse
from scrapy.utils.markup import remove_tags
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

#* Maybe reuse login script and put functions in separate files and call all from main.py

# main.py
# login.py
# codes.py
# detail.py
# barcodes.py


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
        # or select code from barcode table - really not sure atm

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
    
        #* Get Big image from Popup
        picturePopup = 'https://www.booker.co.uk' + response.css('.pip a::attr(href)').split("'")[1] # not sure if strip works here
        self.driver.execute_script("window.open('');")
        # not scrapy functions
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(picturePopup)
        imgUrlBig = response.css('img::attr(src)').get_attribute('src').extract_first().strip()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        # End

        #* Add topInfo dict to ItemLoader
        topInfo = dict([
            (
                i.split(':', 1)[0], i.split(':', 1)[1].strip(' %£')
            ) for i in response.css('.pir').text.split('\n')[:-2]
        ])

        wsQuantity, retailSize = topInfo['Size'].split(' x ')

        #* Over complicated (maybe) way of getting description info sections and putting them into a dict
        productDetail = data.find_elements_by_class_name("piSection")
        for i in productDetail:
            i = i.text.split('\n')
            if len(i) < 3:
                json_format[i[0]] = i[1]
            elif ":" in i[1]:
                # choose comment-in method to save Categories in nested dictionary
                # json_format[i[0]] = dict([tuple(j.split(':',1)) for j in i[1:]])
                json_format.update(
                    dict([tuple(j.split(':', 1)) for j in i[1:]]))
            elif "Nutrition" in i[0]:
                json_format[i[0]] = dict(
                    [tuple(j.rsplit(' ', 1)) for j in i[1:]])
            elif "Country" in i[0]:
                json_format.update(
                    dict([tuple(j.rsplit(' ', 1)) for j in i[1:]]))
            else:
                json_format[i[0]] = i[1:]
        # End

        #* Once script runs verify where more scrapy tricks can be employed to make code better 
        # remove_tags()
        # extract_first().strip()

        #* Add these to ItemLoader
        'imgUrlBig': imgUrlBig,
        'imgUrlSmall': response.css('.pir .piTopInfo img::attr(src)').extract_first().strip(),
        'shelfCode': [int(s) for s in re.findall(r'\d\d\d\d\d\d', response.request.url)][1],
        'retailSize': retailSize,
        'wsQuantity': wsQuantity

        #* More work to decide where these go
        "Case of": "a[href*=\"Case\"]", # 15
        "By Product Category ": "a[href*=\"Product\"]", # Core catering (is this cat or sub_cat)

        # Explore difference between xpath and css selector

        l = ItemLoader(item=BookerProductItem(), response=response)
        l.add_css('code', '.pip .pir ul li:contains(Code: ) span')
        # need to use name cleaning
        l.add_css('name', '.pir h3::text()')
        # can be found on left side nav panel
        l.add_css('cat_id', 'selector')
        l.add_css('sub_cat_id ', 'selector')
        l.add_css('shelf_id ', 'selector')
        # All come from list but list changes length so can't reply on index
        l.add_css('wsp_exl_vat', '.pip .pir ul li:contains(WSP: ) span')
        l.add_css('wsp_inc_vat', '.pip .pir ul li:contains(WSP inc VAT: ) span')
        l.add_css('rrp', '.pip .pir ul li:contains(RRP: ) span')
        l.add_css('por', '.pip .pir ul li:contains(POR: ) span')
        l.add_css('vat', '.pip .pir ul li:contains(VAT: ) span')
        l.add_css('size', '.pip .pir ul li:contains(Size: ) span')
        l.add_css('ws_qty', 'selector')
        l.add_css('rt_qty', 'selector')
        l.add_css('pack_type', 'a[href*=\"By+Pack+Type\"]')
        l.add_css('unit_description', '.pip .pir ul li:contains(Unit Description: ) span')
        l.add_css('on_offer', 'a[href*=\"On+Offer\"]')
        l.add_css('additives', 'a[href*=\"By+Additives\"]')
        l.add_css('img_small_guid', 'selector')
        # from popup
        l.add_css('img_big_guid', 'selector')
        l.add_css('brand', '.pip #catLinks b:contains(By Brand:) + span a')
        # Again maybe iterate over dict of possible names in list
        l.add_css('origin_country', 'a[href*=\"By+Country+of+Origin\"]')
        l.add_css('packed_country', 'a[href*=\"By+Packed+In\"]')
        l.add_css('storage_type', 'a[href*=\"By+Storage+Type\"]')
        l.add_css('beverage_type', 'a[href*=\"By+Beverage+Type\"]')
        l.add_css('alcohol_volume', '.pip .pir ul li:contains(Alcohol by Volume: ) span')
        l.add_css('alcohol_units', 'selector')
        # Get below descriptive statements as dict maybe
        l.add_css('description', 'h1:contains(\"Description\") + p')
        l.add_css('allergy_advice', 'h1:contains(\"Allergy Advice\") + ul li')
        l.add_css('ingredients', 'h1:contains(\"Ingredients\") + ul li')
        # Work out how to save unpredictable table - maybe as html string
        l.add_css('nutrition_table', 'h1:contains(\"Nutrition\") + div table') # HTML table might stringify
        l.add_css('nutrition_notes', 'h1:contains(\"Nutrition\") + div + p')
        l.add_css('manufacturer', 'h1:contains(\"Manufacturer\") + p')
        l.add_css('packaging', 'h1:contains(\"Packaging\") + ul li')
        l.add_css('alternative_products', 'h1:contains(\"Alternative Products\") + span + ul li a::attr(href)')
        l.add_css('prepare_and_use', 'h1:contains(\"Prepare and Use\") + p')
        l.add_css('storage_information', 'h1:contains(\"Storage Information\") + ul li')
        l.add_css('freezing_guidelines', 'h1:contains(\"Freezing Guidelines\") + ul li')
        l.add_css('additional_information', 'h1:contains(\"Additional Information\") + p')
        l.add_css('recycling', 'h1:contains(\"Recycling\") + ul li')
        l.add_css('tasting_notes', 'h1:contains(\"Tasting Notes\") + p')
        l.add_css('current_vintage', 'a[href*=\"By+Current+Vintage\"]')
        l.add_css('wine_colour', 'a[href*=\"By+Wine+Colour\"]')
        l.add_css('producer', 'a[href*=\"By+Producer\"]')
        l.add_css('grape_variety', 'a[href*=\"By+Grape+Variety\"]')
        l.add_css('closure_type', 'a[href*=\"By+Type+of+Closure\"]')
        l.add_css('wine_maker', 'a[href*=\"By+Wine+Maker\"]')

        #* Complicated SQL here to see if values are in other table and if they already are then get the id otherwise at it in
        # can't insert "Craft beer" from scraper - have to search "cat" table for cat_name column if beer is there get ID cat_id otherwise insert and get id of newly inserted row


        #* Decisions

        # Bit much overhead having field names defined in SQl and in scrapy item.py and also in ItemLoader and also in SQL insert column names.
        # Maybe bin scrapy BookerItem and ItemLoader and iterate over keys and values using method from below:

        "https://riptutorial.com/scrapy/example/28697/connecting-and-bulk-inserting-to-mysql-in-scrapy-using-mysqldb-module---python-2-7"
    
        self.placeholders = ', '.join(['%s'] * len(item))
        self.columns = ', '.join(item.keys())
        self.query = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("table_name", self.columns, self.placeholders)
        self.items.extend([item.values()])
        cursor.executemany(self.query, self.items)


        yield l.load_item()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BookerProductDetail)
    process.start()



