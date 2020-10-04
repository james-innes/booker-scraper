import json

from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy import Spider, Item, Field
from scrapy.settings import Settings
import html2text


class BookerItem(Item):
    title = Field()
    # link = Field()
    # desc = Field()
    everything = Field()
    dummy = Field()


# define an item loader with input and output processors
class BookerItemLoader(ItemLoader):

    # everything = Field(
    #     input_processor=MapCompose(remove_tags),
    #     output_processor=TakeFirst(),
    # )

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
    allowed_domains = ["booker.co.uk"]
    start_urls = [
        "https://www.booker.co.uk/catalog/products.aspx?categoryName=CS13_200020&view=GroupedByShelf&multi=False"
    ]

    # def parse(self, response):
    #     for sel in response.css('.pr'):
    #         l = BookerItemLoader(BookerItem(), selector=sel, response=response)
    #         l.add_css('title', '.info_r1 a::text')
    #         yield l.load_item()

    # def parse(self, response):
    #     l = BookerItemLoader(BookerItem(), response=response)
    #     l.add_css('title', '.info_r1 a::text')

    #     l.add_value('dummy', 'This is just a test')

    #     sample = response.css('.resultTable')

    #     converter = html2text.HTML2Text()
    #     converter.ignore_links = True
    #     final = converter.handle(sample)  # Python 3 print syntax

    #     l.add_value('everything', final)

    #     yield l.load_item()

    def parse(self, response):
        sample = response.css('div')
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        print(converter.handle(sample))  # Python 3 print syntax


# instantiate settings and provide a custom configuration
settings = Settings({
    'ITEM_PIPELINES': {
        '__main__.JsonWriterPipeline': 100
    }
})

process = CrawlerProcess(settings)
process.crawl(BookerSpider)
process.start()
