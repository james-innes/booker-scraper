BOT_NAME = 'booker'
SPIDER_MODULES = ['booker.spiders']
NEWSPIDER_MODULE = 'booker.spiders'
ROBOTSTXT_OBEY = True
FEED_EXPORTERS = {
    'csv': 'booker.csvexporter.QuoteAllCsvItemExporter',
}
TELNETCONSOLE_ENABLED = False
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}
ITEM_PIPELINES = {
    'booker.pipelines.ProductPipeline': 300,
}
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True