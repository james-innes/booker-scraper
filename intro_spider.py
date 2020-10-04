import scrapy

filename = "book_titles.txt"  # To save store data

class IntroSpider(scrapy.Spider):
    name = "intro_spider"     # Name of the scraper

    def start_requests(self):
        urls = [
            'http://books.toscrape.com/catalogue/page-{x}.html'.format(x=x) for x in range(1, 10)   # x denotes page number
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        book_list = response.css('article.product_pod > h3 > a::attr(title)').extract()  # accessing the titles

        with open(filename, 'a+') as f:   # Writing data in the file
            for book_title in book_list:
                f.write(book_title + "\n")