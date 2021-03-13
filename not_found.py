import requests
import sqlite3

con = sqlite3.connect('stores.db')
cur = con.cursor()
product_detail = cur.execute("SELECT * FROM product_detail").fetchall()
con.close()

not_found = []

for product in product_detail:
    code = product[0]
    img = product[1]

    r = requests.get(f"https://www.booker.co.uk/bbimages{img}")

    if r.status_code == 404:
        print(f"Not Found for code: {code}")
        not_found.append([code])

con = sqlite3.connect('stores.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS not_found")
cur.execute("CREATE TABLE not_found(code INTEGER)")
cur.executemany("INSERT INTO not_found(code) VALUES(?)", not_found)
con.commit()
con.close()
