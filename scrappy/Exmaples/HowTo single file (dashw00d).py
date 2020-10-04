#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy import Spider, Item, Field
from scrapy.settings import Settings

# Originally built off of:
# https://gist.github.com/alecxe/fc1527d6d9492b59c610


def extract_tag(self, values):
    # Custom function for Item Loader Processor
    for value in values:
        yield value[5:-1]


class DefaultAwareItem(Item):
    # Converts field default meta into default value fallback
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use python's built-in setdefault() function on all items
        for field_name, field_metadata in self.fields.items():
            if not field_metadata.get('default'):
                self.setdefault(field_name, 'No default set')
            else:
                self.setdefault(field_name, field_metadata.get('default'))


# Item Field
class CustomItem(DefaultAwareItem):
    '''
    Input / Output processors can also be declared in the field meta, e.g —

    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    '''

    title = Field(default="No Title")
    link = Field(default="No Links")
    desc = Field() # Left blank to test default awareness
    tag = Field(default="No Tags")


class CustomItemLoader(ItemLoader):
    '''
    Item Loader declaration — input and output processors, functions
    https://doc.scrapy.org/en/latest/topics/loaders.html#module-scrapy.loader.processors

    Built-in Processors (Most common place to apply functions to items)
    Identity() - leaves as is
    TakeFirst - Takes first non null value
    Join() - basically equivelent to u' '.join
    Compose() - applies a list of functions one at a time **accepts loader_context
    MapCompose() - applies a list of functions to a list of objects **accepts loader_context \
        first function is applied to all objects then altered objects to next function etc..

    https://doc.scrapy.org/en/latest/topics/loaders.html#declaring-input-and-output-processors
    _in processors are applied to extractions as soon as received
    _out processors are applied to collected data as loader.load_item() is yielded
    Single items are always converted to iterables
    Custom processing functions must receive self and one positional input for values
    '''

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    desc_out = Join()
    tag_in = extract_tag  # function assigned as class variable
    tag_out = Join(', ')


# Define a pipeline
class WriterPipeline(object):
    def __init__(self):
        self.file = open('items.txt', 'w')

    def process_item(self, item, spider):
        self.file.write(item['title'] + '\n')
        self.file.write(item['link'] + '\n')
        self.file.write(item['desc'] + '\n')
        self.file.write(item['tag'] + '\n\n')
        return item


# Define a spider
class CustomSpider(Spider):
    name = 'single_spider'
    allowed_domains = ['dashwood.net']
    start_urls = ['https://dashwood.net/']

    def parse(self, response):
        for sel in response.xpath('//article'):

            loader = CustomItemLoader(
                CustomItem(), selector=sel, response=response)
            loader.add_xpath('title', './/h2/a/text()')
            loader.add_xpath('link', './/a/@href')
            loader.add_xpath('desc', './/p/text()')
            loader.add_xpath('tag', './/a[@class="tag"]//@href')

            yield loader.load_item()


# Declare some settings / piplines
settings = Settings({
    # Piplines start with the project/module name so replace with __main__
    'ITEM_PIPELINES': {
        '__main__.WriterPipeline': 100,
    },

    'DEFAULT_REQUEST_HEADERS': {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'
    },

    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    }
})

process = CrawlerProcess(settings)

# You can run 30 of these at once if you want, e.g —
# process.crawl(CustomSpider)
# process.crawl(CustomSpider) etc.. * 30
process.crawl(CustomSpider)
process.start()