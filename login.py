
import os, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()
print("Be patient :)")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://www.booker.co.uk/home')

driver.find_element_by_id('CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'), Keys.RETURN)
time.sleep(2)
driver.find_element_by_id('Email').send_keys(os.getenv('BOOKER_EMAIL'))
driver.find_element_by_id('Password').send_keys(os.getenv('BOOKER_PASSWORD'), Keys.RETURN)
time.sleep(3)

# Elevate permissions for Barcode page
driver.get('https://www.booker.co.uk/products/product-list?categoryName=CS13_100001')
driver.find_element_by_css_selector('a.print-btn').click()
driver.find_element_by_css_selector('a[href*="print-product-list-ungroup"]').click()

time.sleep(1)
print("ASP_NET_SESSION: " + driver.get_cookie('ASP.NET_SessionId')['value'])
print("ASPXAUTH: " + driver.get_cookie('.ASPXAUTH')['value'])

driver.quit()
