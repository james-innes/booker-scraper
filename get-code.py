import json

from scrapy.crawler import CrawlerProcess
from scrapy import Spider
from scrapy.settings import Settings
from scrapy.shell import inspect_response


class BookerSpider(Spider):
    name = "Booker"
    allowed_domains = ["booker.co.uk"]
    start_urls = [
        "https://www.booker.co.uk/catalog/productinformation.aspx?code=134840&settype=13&categoryName=300350&CSUrl=https%3a%2f%2fwww.booker.co.uk%2fcatalog%2fproducts.aspx%3fcategoryName%3dCS13_200070%26view%3dUnGrouped%26multi%3dFalse"
    ]

    def parse(self, response):
        print('\n')
        print("HERE:")
        print(response.css(".headerSearchLabel ::text").get())
        print('\n')


process = CrawlerProcess()
process.crawl(BookerSpider)
process.start()
