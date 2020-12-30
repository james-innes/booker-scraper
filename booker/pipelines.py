
from itemadapter import ItemAdapter
import re

class ProductPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        name = adapter.get('name')[0]

        subs = [
            r'/\?ÕÌ_|_Œ‚|[ŠŽÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÞßðÿ_]+',
            r'.PMP\s?£?(\d+.?\d+)',  # "PMP £3.29"
            r'(\d+)\s?x\s?',  # Remove "36 x "
            r'/[^\x00-\x7F]|\?',
            r'retail\s/gi' # Remove "Retail"
            r'.\([0-9]+[a-z]{0,2}\)' # "Drink 100g (800g)" -> "Drink 100g"
        ]

        for rgx in subs:
            name = re.sub(rgx, '', name)

        adapter['name'] = name
        return item
