
import os, time, csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import sqlite3
from dotenv import load_dotenv

load_dotenv()
options = Options()
options.headless = True
d = webdriver.Firefox(options=options)
d.get('https://www.booker.co.uk/home')

d.find_element_by_id('CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'), Keys.RETURN)
time.sleep(2)
d.find_element_by_id('Email').send_keys(os.getenv('BOOKER_EMAIL'))
d.find_element_by_id('Password').send_keys(os.getenv('BOOKER_PASSWORD'), Keys.RETURN)
time.sleep(3)

with open('barcode.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, fieldnames=['barcode', 'code', 'sub_cat_code'])
  writer.writeheader()

  for row in [["CS13_201630", "Pet Food", "Cats"], ["CS13_201640", "Pet Food", "Dogs"]]:
    d.get(f'https://www.booker.co.uk/products/product-list?categoryName={row[0]}')
    d.get(f'https://www.booker.co.uk/products/print-product-list-ungroup?printType=ProductList')

    for tr in d.find_elements_by_css_selector('.table-desktop tbody tr'):
      writer.writerow({
        'barcode': tr.find_element_by_tag_name('svg').get_attribute('jsbarcode-value'),
        'code': tr.find_element_by_css_selector('td:nth-of-type(2)').text,
        'sub_cat_code': row[0],
      })

d.quit()