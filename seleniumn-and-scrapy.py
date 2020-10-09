from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from scrapy.crawler import CrawlerProcess
from scrapy import Spider, Request
from scrapy.settings import Settings


class BookerSpider(Spider):
    name = "Booker"
    allowed_domains = ["booker.co.uk"]
    start_urls = [
        "https://www.booker.co.uk/catalog/mybooker.aspx"
    ]

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(
            "https://www.booker.co.uk/account/loginregister/UserLogin.aspx")
        self.driver.find_element_by_id("LoginControl_CustomerNumberSingle").send_keys(
            "BOOKER_ACCOUNT")
        self.driver.find_element_by_id(
            "LoginControl_EnterCustomerNumberSubmit").click()
        time.sleep(0.5)
        self.driver.find_element_by_id(
            "LoginControl_EmailSingle").send_keys("BOOKER_EMAIL")
        self.driver.find_element_by_id(
            "LoginControl_PasswordSingle").send_keys("BOOKER_PASSWORD")
        self.driver.find_element_by_id(
            "LoginControl_EnterEmailPasswordSubmit").click()

        yield Request("https://www.booker.co.uk/catalog/mybooker.aspx", self.find_something)

    def find_something(self, response):
        print('\n')
        print("HERE:")
        ####### THE PROBLEM: Seleniumn is on Home Page and Scrapy is still on UserLogin page #######
        print(response.css('span#ButcheryDepartment_ctl01_ButcherName::text'))
        print(response.css('#LoginControl_TitleCustomerNumber::text'))
        print('\n')

        self.driver.close()


process = CrawlerProcess()
process.crawl(BookerSpider)
process.start()
