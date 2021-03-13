import requests
import sqlite3
import pandas as pd

product_detail = sqlite3.connect('stores.db').execute("SELECT * FROM product_detail").fetchall()
not_found = []

for product in product_detail:
    code = product[0]
    img = product[1]

    r = requests.get(f"https://www.booker.co.uk/bbimages{img}")

    if r.status_code == 404:
      print(f"Not Found for code: {code}")
      not_found.append(code)

pd.DataFrame(not_found, columns=["code"]).to_csv('notfound.csv', index=False)