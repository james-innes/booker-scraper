
import csv
import re

#* Read names from csv and only work with a number of the rows 

# with open('testing-names.csv', "r", newline='') as f:
#     reader = csv.DictReader(f)
#     for index, row in zip(range(50), reader):

#*Instead of csv just inline names

samples = [
    "Tiger Asian Lager Beer 24 x 330ml Bottles",
    "Budweiser 4.5%",
    "Greene King IPA 500ml",
    "Chef's Larder Texan 100% Beef Burgers 48 x 113g (5.42kg)",
    "Pearl Delights 26/30 Raw, Peeled and Deveined King Prawns 900g net (Drained Weight 900kg)",
    "Smirnoff Ice Vodka Mixed Drink 70cl Bottle PMP £3.29",
    "Smirnoff Ice Vodka Mixed Drink 70cl Bottle PMP Â£3.29"
]

#* Get rid of wholesale qty and other rubbish from product names

substitutions = [
    r'.PMP\s?£?(\d+.?\d+)',
    r'(\d+)\s?x\s?',
    r'/\?ÕÌ_|_Œ‚|[ŠŽÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÞßðÿ_]+/gi',
    r'/[^\x00-\x7F]|\?/g'
]

for sample in samples:
    for rgx in substitutions:
        result = re.sub(rgx, '', sample)

    print(result)


# # Remove "36 x "
# first = re.sub(r'(\d+)\s?x\s?', '', title)
# print(first)

# Remove PMP "PMP £3.29"
# second = re.sub(r'.PMP\s?£?(\d+.?\d+)', 'hellop ', row['name'])
# print(second)

# result = re.sub(r{}, '', row['name']).sub(r'', '')

# print(result)


# Where y x y replace " x whatever" with nothing


# replacements = [
#     ('__this__', 'something'),
#     ('__This__', 'when'),
#     (' ', 'this'),
#     ('.', 'is'),
#     ('__', 'different')
# ]

# for old, new in replacements:
#     stuff = re.sub(old, new, stuff)

# stuff = stuff.capitalize()
