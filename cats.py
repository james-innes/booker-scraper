import re
import sqlite3
import pandas as pd

cats = sqlite3.connect('stores.db').execute("SELECT * FROM catalog_cats").fetchall()
new_cats = []

replacements = [
	[r'Dogs', 'Dog Food'],
	[r'Cats', 'Cat Food'],
	[r'Dishwasher and Washing Up', 'Washing Up'],
	[r'Car Care, DIY, Maintenance', 'Care Care'],
	[r'Car Care, DIY, Maintenance', 'Care Care'],
	[r'Cooked Meat and Sausages', 'Meat & Sausages'],
	[r'Cookware and Kitchen Equipment', 'Kitchen Equipment'],
	[r'On Premise', 'More Drinks'],
	[r'Pastry, Savouries, Bread and Pasta', 'Bread, Pastry, & Pasta'],
	[r'Salads, Sandwich Fillers, Dips', 'Salads, Sandwich, Dips'],
	[r'\sand\s', ' & '],
	[r'.?Catering', ''],
	[r'.?Retail(er)?.?', ''],
	[r'.?Professional', ''],
]

for cat in cats:
		new_cat = cat[0]
		for find, replace in replacements:
				new_cat = re.sub(find, replace, new_cat, flags=re.IGNORECASE)
		new_cats.append(new_cat)

pd.DataFrame(new_cats, columns=["cat"]).to_csv('cats.csv', index=False)