
import re
import pandas as pd
import numpy as np

df = pd.read_csv('catalog.csv')

substitutions = [
    r'/\?ÕÌ_|_Œ‚|[ŠŽÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÞßðÿ_]+',
    r'.PMP\s?£?(\d+.?\d+)',  # "PMP £3.29"
    r'(\d+)\s?x\s?',  # Remove "36 x "
    r'/[^\x00-\x7F]|\?'
]

# TODO:
# Remove "Retail "
# Ensure items with no image or price
# id no RRP then use markup on wholesale price

for index, row in df.iterrows():
    for rgx in substitutions:
        row[2] = re.sub(rgx, '', row[2])

    df.at[index, "name"] = row[2]

df.to_csv("catalog.csv", index=False)
