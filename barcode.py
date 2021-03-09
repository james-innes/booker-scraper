import os, time, csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import sqlite3
from dotenv import load_dotenv

load_dotenv()
print("Scraping Barcodes...")
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

  for row in sqlite3.connect('stores.db').execute("SELECT * FROM sitemap").fetchall():
  # for row in [["CS13_201630", "Pet Food", "Cats"], ["CS13_201640", "Pet Food", "Dogs"]]:
  # for row in [["CS13_200020", "Beer and the rest", "Cider"]]:
    d.get(f'https://www.booker.co.uk/products/product-list?categoryName={row[0]}')
    page_count = len(d.find_elements_by_css_selector('.page-link[rel=next]'))

    for page_index in (range(page_count) if page_count > 0 else range(1)):
      d.get(f'https://www.booker.co.uk/products/product-list?categoryName={row[0]}&pageIndex={page_index}')
      d.get(f'https://www.booker.co.uk/products/print-product-list-ungroup?printType=ProductList')

      for tr in d.find_elements_by_css_selector('.table-desktop tbody tr'):
        try:
          barcode = tr.find_element_by_tag_name('svg').get_attribute('jsbarcode-value')
        except:
          barcode = ""

        writer.writerow({
          'barcode': barcode,
          'code': tr.find_element_by_css_selector('td:nth-of-type(2)').text,
          'sub_cat_code': row[0],
        })

d.quit()