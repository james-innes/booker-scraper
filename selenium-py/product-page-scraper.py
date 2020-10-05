from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

import csv
import json
import time
import re


driver = webdriver.Firefox(
    executable_path=GeckoDriverManager().install())

# Login
driver.get(
    "https://www.booker.co.uk/account/loginregister/UserLogin.aspx")
driver.find_element_by_id("LoginControl_CustomerNumberSingle").send_keys(
    "***REMOVED***")
driver.find_element_by_id(
    "LoginControl_EnterCustomerNumberSubmit").click()
time.sleep(0.5)
driver.find_element_by_id(
    "LoginControl_EmailSingle").send_keys("***REMOVED***")
driver.find_element_by_id(
    "LoginControl_PasswordSingle").send_keys("drvLNXzExJ6J96zn")
driver.find_element_by_id(
    "LoginControl_EnterEmailPasswordSubmit").click()

with open('data/products-list.csv', "r", newline='') as f:
    reader = csv.DictReader(f)
    with open('data/products-detail.csv', 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=['retailSize', 'wsQuantity', 'shelfCode', 'imgUrlSmall', 'imgUrlBig', 'catCode', 'catName', 'subCatCode', 'subCatName', 'name', 'VAT', 'Size', 'WSP inc VAT', 'WSP', 'Code', 'Alcohol by Volume', 'RRP', 'POR', 'Alcohol Units', 'Unit Description', 'url'])
        writer.writeheader()

        for row in reader:
            driver.get(row['url'])
            d = driver.find_element_by_class_name("pip")

            # Get Big Picture from Popup
            picturePopup = "https://www.booker.co.uk" + \
                d.find_element_by_css_selector(
                    'a').get_attribute('href').split("'")[1]
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(picturePopup)
            imgUrlBig = driver.find_element_by_css_selector(
                'img').get_attribute('src').split("'")[0]
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            topInfo = dict([
                (
                    i.split(':', 1)[0], i.split(':', 1)[1].strip(" %£")
                ) for i in d.find_element_by_css_selector(".pir").text.split('\n')[:-2]
            ])

            wsQuantity, retailSize = topInfo['Size'].split(' x ')

            product = dict({
                'catCode': row['catCode'],
                'catName': row['catName'],
                'subCatCode': row['subCatCode'],
                'subCatName': row['subCatName'],
                'url': row['url'],
                'name': d.find_element_by_tag_name("h3").text,
                'imgUrlBig': imgUrlBig,
                'imgUrlSmall':
                    d.find_element_by_css_selector(
                        '.piTopInfo img').get_attribute('src').split("'")[0],
                'shelfCode': [int(s) for s in re.findall(r'\d\d\d\d\d\d', row['url'])][1],
                'retailSize': retailSize,
                'wsQuantity': wsQuantity
            })

            product.update(topInfo)
            writer.writerow(product)


driver.quit()
