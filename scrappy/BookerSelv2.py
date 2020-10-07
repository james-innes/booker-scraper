# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# ! Firefox has been used for webdriver ! #

import os
from selenium import webdriver
import time
from urllib.parse import urljoin

from scrapy.crawler import CrawlerProcess
from scrapy import Spider, Request
from scrapy.http import FormRequest
from scrapy.settings import Settings
from scrapy.shell import inspect_response
from scrapy import Selector
from scrapy.http import HtmlResponse
	
custno=os.environ.get('booker_customer')
email=os.environ.get('booker_email')
passw=os.environ.get('booker_password')

class LoginSpider2(Spider):
    header = {"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/33.0"}
    name = "booker_mb"
    custom_settings = {"FEEDS": {"booker.csv":{"format":"csv"}}}
    allowed_domains = ["booker.co.uk"]
    start_urls = ['https://www.booker.co.uk/home.aspx']
    
    def __init__(self):
		# Use  Selenium to log in and get a response for Scrapy
        self.custno=os.environ.get('booker_customer')
        self.email=os.environ.get('booker_email')
        self.passw=os.environ.get('booker_password')
        self.driver = webdriver.Firefox()
        
        self.driver.get('https://www.booker.co.uk/home.aspx')
        self.driver.find_element_by_id ('OutsideHomePageControl_CustomerNumber').send_keys(self.custno)
        self.driver.find_element_by_id('OutsideHomePageControl_cmdCustomerNumber').click()
        print(self.driver.title)
        time.sleep(2)
             
        self.driver.find_element_by_id ('LoginControl_EmailSingle').send_keys(self.email)
        self.driver.find_element_by_id ('LoginControl_PasswordSingle').send_keys(self.passw)
        self.driver.find_element_by_id('LoginControl_EnterEmailPasswordSubmit').click()
        
    def parse(self, response):
		# Gets the Selenium response and passes to Scrapy to parse/crawl
        self.driver.get(response.url)
        res = response.replace(body=self.driver.page_source)
        logged_in_page = (res.body)
        print('logged_in_page')

        
        for page in res.css('a'):
            yield {
                'url-href': page.xpath('@href').extract(),
                'url-text': page.css('::text').extract()
                }

        view_state = response.xpath('//*[@id="Form1"]/input[@name="__VIEWSTATE"]/@value').get() #

        products_link = res.xpath('//a[contains(@href,"/catalog/products.aspx")]/@href').get()    
        print(products_link)
        
        # Logged in, and at home page
        
        products="https://www.booker.co.uk/catalog/products.aspx"
        next_url = products
        
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'BookerEU=1; __utmz=127566494.1597660464.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); BookerMessage=WebsiteBulletinCheckedDate=17%2f08%2f2020+11%3a34%3a29; s_fid=58567D4770E7E84E-24F4000103726761; Commerce_TestPersistentCookie=TestCookie; Booker=Guid=%7b1406f591-9b3a-4788-8d72-0e714b102fdc%7d; Commerce_TestSessionCookie=TestCookie; ASP.NET_SessionId=hoxyuigmv3ufirmjfj0l3fqd; __utma=127566494.312950862.1597660464.1601982470.1601991696.7; __utmc=127566494; __utmv=127566494.Schools%20%2F%20Colleges%20%2F%20University; sc_loginStatus=( logout ); s_cc=true; gpv_pn=home%3Amybooker; CampaignHistory=8802,8797,8799,8798,13219,8801,10782,12379,30397,27942,25436,12460,30402,29716,12379,30397,27942,25436,12460,30402,29716,12379,30397,27942,25436,12460,30402,29716,12379,30397,27942,25436,12460,30402,29716; __utmt=1; __utmb=127566494.24.10.1601991696; s_sq=tescobookerwebprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhome%25253Amybooker%2526link%253DProducts%2526region%253Dt1%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dhome%25253Amybooker%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.booker.co.uk%25252Fcatalog%25252Fproducts.aspx%2526ot%253DA',
            'Host': 'www.booker.co.uk',
            'Referer': 'https://www.booker.co.uk/catalog/mybooker.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            }
                
        request = FormRequest(url=next_url, headers=headers ,callback=self.parse2)
        yield request      
             
    def parse2(self, response):
    
        print("\n## Now on Products Page of 24 thumbnails menu ##")
        print("\n## Now we will go and get BEER ##")
        
        BEER = 'https://www.booker.co.uk/catalog/products.aspx?categoryName=Default%20Catalog&keywords=beer&view=UnGrouped'
        
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '2660',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'BookerEU=1; __utmz=127566494.1597660464.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); BookerMessage=WebsiteBulletinCheckedDate=17%2f08%2f2020+11%3a34%3a29; s_fid=58567D4770E7E84E-24F4000103726761; Commerce_TestPersistentCookie=TestCookie; Booker=Guid=%7b1406f591-9b3a-4788-8d72-0e714b102fdc%7d; Commerce_TestSessionCookie=TestCookie; ASP.NET_SessionId=hoxyuigmv3ufirmjfj0l3fqd; __utmc=127566494; __utmv=127566494.Schools%20%2F%20Colleges%20%2F%20University; sc_loginStatus=( logout ); s_cc=true; __utma=127566494.312950862.1597660464.1601991696.1602002332.8; __utmt=1; s_sq=%5B%5BB%5D%5D; CampaignHistory=19048,13219,28968,12979,11055,11576,10782,8803,8800,8799,25954,8801,8798,8797,25436,12460,30402,8796,25210,11055,8799,8802,8800,25954,19048,10782,8803,13219,11576,8801,28968,12979,9118,8797,8798; __utmb=127566494.3.10.1602002332; gpv_pn=browse%3Aall',
            'Host': 'www.booker.co.uk',
            'Origin': 'https://www.booker.co.uk',
            'Referer': 'https://www.booker.co.uk/catalog/products.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'  
            }
        
        request = Request(url=BEER,callback=self.beer)
        yield request      
        
    def beer(self, response):
        #print("\n## Now we have BEER! - here is the raw html ##")
        #print(response.body)
        
        print("\n## Get link to each product page")
        result = response.css("tr .info_r1 a::attr(href)").extract()
        yield{'link':result}
        
        # The html looks pretty messy - Are you good with regex ?
        # I don't know how long cookies last - they may expire and need updating in this code in due course?
        
# Main Driver 
if __name__ == "__main__":
	process = CrawlerProcess()
	process.crawl(LoginSpider2)
	process.start()

