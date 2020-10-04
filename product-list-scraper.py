from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

import csv
import json
import time
import re


driver = webdriver.Firefox(
    executable_path=GeckoDriverManager().install())


driver.get(
    "https://www.booker.co.uk/account/loginregister/UserLogin.aspx")
driver.find_element_by_id("LoginControl_CustomerNumberSingle").send_keys(
    "303182030")
driver.find_element_by_id(
    "LoginControl_EnterCustomerNumberSubmit").click()
time.sleep(0.5)
driver.find_element_by_id(
    "LoginControl_EmailSingle").send_keys("nigelsr@gmail.com")
driver.find_element_by_id(
    "LoginControl_PasswordSingle").send_keys("drvLNXzExJ6J96zn")
driver.find_element_by_id(
    "LoginControl_EnterEmailPasswordSubmit").click()


with open('products-list.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=['catCode', 'catName', 'subCatCode', 'subCatName', 'url'])
    writer.writeheader()

    with open('sitemap.json') as json_file:
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
