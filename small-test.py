import json

from scrapy.crawler import CrawlerProcess
from scrapy import Spider
from scrapy.settings import Settings
from scrapy.shell import inspect_response


class BookerSpider(Spider):
    name = "Booker"
    allowed_domains = ["booker.co.uk"]
    start_urls = [
        "https://www.booker.co.uk/account/loginregister/UserLogin.aspx"
    ]

    def parse(self, response):
        print('\n')
        print("HERE:")
        print(response.css('#LoginControl_TitleCustomerNumber::text'))
        print('\n')


process = CrawlerProcess()
process.crawl(BookerSpider)
process.start()
