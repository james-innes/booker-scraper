import json

with open ('sitemap.json') as j:
    bookerdict = json.load(j)
  

def flatten_json(jsondict):
    d = {}
    mylist = bookerdict['categories']
    for names in mylist:
        #print (names['name'])
        dictnames = (names['subCategories'])
        #print(dictnames)
        for i in dictnames:
            for k,v in i.items():
                print (v)
        

print(flatten_json(bookerdict))
