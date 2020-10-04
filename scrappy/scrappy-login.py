import json

from scrapy.crawler import CrawlerProcess
from scrapy import Spider, FormRequest, Request
from scrapy.settings import Settings
from scrapy.shell import inspect_response
# from scrapy.utils.response import open_in_browser


class LoginSpider(Spider):
    name = "Booker"
    allowed_domains = ["booker.co.uk"]
    start_urls = [
        "https://www.booker.co.uk/account/loginregister/UserLogin.aspx"
    ]

    def parse(self, response):
        return FormRequest.from_response(
            response,
            # formid='LoginControl_CustomerNumberSingle',
            formdata={
                'LoginControl$CustomerNumberSingle': '303182030'
            },
            callback=self.after_customer_number
        )

    def after_customer_number(self, response):
        return FormRequest.from_response(
            response,
            formdata={
                '__VIEWSTATEGENERATOR': 'E026D3EE',
                'LoginControl$EmailSingle': 'nigelsr@gmail.com',
                'LoginControl$PasswordSingle': 'drvLNXzExJ6J96zn',
                'LoginControl$EnterEmailPasswordSubmit.x': '55',  # may be dynamically created
                'LoginControl$EnterEmailPasswordSubmit.y': '74'  # may be dynamically created
            },
            callback=self.after_email_and_password
        )

    def after_email_and_password(self, response):
        # check login succeed before going on
        # if "authentication failed" in response.body:
        #     self.logger.error("Login failed")
        #     return

        # sample = response.css("div")
        # print(sample)

        # print(response.text)
        # open_in_browser(response)

        print('\n')
        print("HERE:")
        print(response.css('span#ButcheryDepartment_ctl01_ButcherName::text')) # Home Page
        print(response.css('#LoginControl_TitleCustomerNumber::text')) # UserLogin Page
        print(response.css('.pip h3 ::text')) # Product page
        print('\n')

        ##### Can't navigate away from UserLogin page ######

        url = "https://www.booker.co.uk/catalog/productinformation.aspx?code=134840&settype=13&categoryName=300350&CSUrl=https%3a%2f%2fwww.booker.co.uk%2fcatalog%2fproducts.aspx%3fcategoryName%3dCS13_200070%26view%3dUnGrouped%26multi%3dFalse"
        yield Request(url, self.parse_page)

    def parse_page(self, response):
        print('\n')
        print("HERE:")
        print(response.css('span#ButcheryDepartment_ctl01_ButcherName::text')) # Home Page
        print(response.css('#LoginControl_TitleCustomerNumber::text')) # UserLogin Page
        print(response.css('.pip h3 ::text')) # Product page
        print('\n')


process = CrawlerProcess()
process.crawl(LoginSpider)
process.start()
