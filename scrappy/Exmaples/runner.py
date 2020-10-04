import json

from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy import Spider, Item, Field
from scrapy.settings import Settings


class BookerItem(Item):
    title = Field()
    # link = Field()
    # desc = Field()


# define an item loader with input and output processors
class BookerItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    desc_out = Join()


# define a pipeline
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# define a spider
class BookerSpider(Spider):
    name = "Booker"
    allowed_domains = ["dmoztools.net"]
    start_urls = [
        "http://www.dmoztools.net/Computers/Programming/Languages/Python/Books/"
    ]

    def parse(self, response):
        for sel in response.css('.site-item'):
            l = BookerItemLoader(BookerItem(), selector=sel, response=response)
            l.add_css('title', '.site-title::text')
            yield l.load_item()


# instantiate settings and provide a custom configuration
settings = Settings({
    'ITEM_PIPELINES': {
        '__main__.JsonWriterPipeline': 100
    }
})

process = CrawlerProcess(settings)
process.crawl(BookerSpider)
process.start()
