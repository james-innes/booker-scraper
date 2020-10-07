# Author Ali Husnain(fiverr.com/dexteruz)
# Use this link for other browsers, just add code snippnets: https://pypi.org/project/webdriver-manager/
# For install dependencies
# pip install -U selenium webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import json
import time
import re


class login_booker:
    def __init__(self, loginInfo, productURL):
        self.url = productURL
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install())

        # self.driver.minimize_window()
        self.preprocessing()

    def preprocessing(self):
        self.driver.get("https://www.booker.co.uk/home.aspx")
        accNo = self.driver.find_element_by_id(
            "OutsideHomePageControl_CustomerNumber")
        accNo.send_keys(loginInfo[0])
        accNo.send_keys(Keys.RETURN)
        time.sleep(0.5)

        self.driver.get(
            "https://www.booker.co.uk/account/loginregister/UserLogin.aspx")

        email = self.driver.find_element_by_id("LoginControl_EmailSingle")
        email.send_keys(loginInfo[1])

        password = self.driver.find_element_by_id(
            "LoginControl_PasswordSingle")
        password.send_keys(loginInfo[2])

        butLogin = self.driver.find_element_by_id(
            "LoginControl_EnterEmailPasswordSubmit")
        butLogin.click()
        self.start_scraping()

    def start_scraping(self):

        self.link_to_json()
        self.driver.quit()

    def link_to_json(self):
        codes = [int(s) for s in re.findall(r'\d\d\d\d\d\d', self.url)]
        self.driver.get(self.url)

        data = self.driver.find_element_by_class_name("pip")
        # print(data.text)
        title = data.find_element_by_tag_name('h3')

        category = self.driver.find_elements_by_class_name('selected')
        subCategoryCode = category[1].get_attribute("cat")
        category, subCategory = [i.text for i in category][1:]

        img = data.find_elements_by_tag_name('img')
        imgLarge = data.find_element_by_tag_name('a').get_attribute('href')

        imgLarge = "booker.co.uk"+imgLarge.split("'")[1]

        imageSmallGuid = img[0].get_attribute(
            'src').split('/')[-1].split('.')[0]
        prodInfo = data.find_element_by_class_name("pir")
        pibox = data.find_element_by_class_name("pibox")

        productDetail = data.find_elements_by_class_name("piSection")
        disclaimer = data.find_elements_by_class_name("piDisclaimer")

        json_format = {}
        # remove 'Number of Trolley' and 'Add to Shopping list' options
        prodInfo = prodInfo.text.split('\n')[:-2]

        # converting product info to json
        json_format = dict(
            [(i.split(':', 1)[0], i.split(':', 1)[1].strip()) for i in prodInfo])
        json_format['title'] = title.text
        json_format['categoryName'] = category
        json_format['subCategoryName'] = subCategory
        json_format['subCategoryCode'] = subCategoryCode
        json_format['image_url'] = img[0].get_attribute('src')
        json_format['imageSmallGuid'] = imageSmallGuid
        json_format['imageBigGuid'] = imgLarge
        json_format['shelfCode'] = codes[1]
        json_format['WSP inc VAT'] = json_format['WSP inc VAT'].replace(
            "£", '')
        json_format['WSP'] = json_format['WSP'].replace("£", '')
        json_format['RRP'] = json_format['RRP'].replace("£", '')
        wsQuantity, retailSize = json_format['Size'].split('x')
        json_format['wsQuantity'] = wsQuantity
        json_format['retailSize'] = retailSize
        json_format.pop('Size')
        pibox = pibox.text.split('\n')
        json_format[pibox[0]] = pibox[1]

        # converting to product detail to json
        for i in productDetail:
            i = i.text.split('\n')
            if len(i) < 3:
                json_format[i[0]] = i[1]
            elif ":" in i[1]:
                # choose comment-in method to save Categokries in nested dictionary
                ## json_format[i[0]] = dict([tuple(j.split(':',1)) for j in i[1:]])
                json_format.update(
                    dict([tuple(j.split(':', 1)) for j in i[1:]]))
            elif "Nutrition" in i[0]:
                json_format[i[0]] = dict(
                    [tuple(j.rsplit(' ', 1)) for j in i[1:]])
            elif "Country" in i[0]:
                json_format.update(
                    dict([tuple(j.rsplit(' ', 1)) for j in i[1:]]))

            else:

                json_format[i[0]] = i[1:]

        json_format['Nutrition']['per'] = json_format['Nutrition']['(per'][:-1]
        json_format['Nutrition'].pop('(per')
        json_format["Disclaimer"] = '\n'.join([i.text for i in disclaimer])

        # print(json_format)

        j = {}
        j[prodInfo[0].split(":")[-1].strip()] = json_format
        with open('product-info.json', 'w') as f:
            json.dump(j, f)


if __name__ == "__main__":

    loginInfo = ["BOOKER_ACCOUNT", "BOOKER_EMAIL", "BOOKER_PASSWORD"]
    url = "https://www.booker.co.uk/catalog/productinformation.aspx?code=606053&settype=23&categoryName=307954&CSUrl=https%3a%2f%2fwww.booker.co.uk%2fcatalog%2fproducts.aspx%3fcategoryName%3dCS13_200001%26view%3dUnGrouped%26sortField%3dCore%26SortDirection%3dAscending%26multi%3dFalse%26pageIndex%3d3"
    obj = login_booker(loginInfo, url)
