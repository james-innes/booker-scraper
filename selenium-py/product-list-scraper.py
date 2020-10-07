import os
import csv
import json
import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(
    executable_path=GeckoDriverManager().install())


driver.get("https://www.booker.co.uk/account/loginregister/UserLogin.aspx")
driver.find_element_by_id("LoginControl_CustomerNumberSingle").send_keys(
    os.getenv("BOOKER_ACCOUNT"))
driver.find_element_by_id("LoginControl_EnterCustomerNumberSubmit").click()
time.sleep(0.5)

driver.find_element_by_id("LoginControl_EmailSingle").send_keys(
    os.getenv("BOOKER_EMAIL"))
driver.find_element_by_id("LoginControl_PasswordSingle").send_keys(
    os.getenv("BOOKER_PASSWORD"))
driver.find_element_by_id("LoginControl_EnterEmailPasswordSubmit").click()

with open('data/products-list.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=['catCode', 'catName', 'subCatCode', 'subCatName', 'url'])
    writer.writeheader()

    with open('data/sitemap.json') as json_file:
        sitemap = json.load(json_file)

        for cat in sitemap['categories']:
            for subCat in cat['subCategories']:
                driver.get(
                    f"https://www.booker.co.uk/catalog/products.aspx?categoryName={subCat['code']}")

                productList = driver.find_elements_by_css_selector(
                    '.resultTable tbody tr .info_r1 a')

                for product in productList:
                    productLink = product.get_attribute('href')
                    writer.writerow(
                        {
                            'catCode':
                                driver.find_element_by_css_selector(
                                    '.dropdown .selected').get_attribute('cat'),
                            'catName': cat['name'],
                            'subCatCode': subCat['code'],
                            'subCatName': subCat['name'],
                            'url': productLink
                        }
                    )

driver.quit()
