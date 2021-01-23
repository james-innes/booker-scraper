import re
import sqlite3
import pandas as pd

cats = sqlite3.connect('stores.db').execute("SELECT * FROM cats").fetchall()
new_cats = []

replacements = [
	[r'and', '&'],
    [r'.?retail', ''],
    [r'.?professional', ''],
    [r'dog', 'Dog Food'],
    [r'cat', 'Cat Food'],
    [r'Dishwasher and Washing Up', 'Washing Up']
]

for cat in cats:
    new_cat = cat[0]
    for find, replace in replacements:
        new_cat = re.sub(find, replace, new_cat, flags=re.IGNORECASE)
    new_cats.append(new_cat)

pd.DataFrame(new_cats, columns=["cat"]).to_csv('cats.csv', index=False)