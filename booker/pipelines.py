
from itemadapter import ItemAdapter
import re
import lxml.html.clean as clean

class ProductPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        name = adapter.get('name')[0]
        for rgx in [
            r'/\?ÕÌ_|_Œ‚|[ŠŽÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÞßðÿ_]+',
            r'.PMP\s?£?(\d+.?\d+)',  # "PMP £3.29"
            r'(\d+)\s?x\s?',  # Remove "36 x "
            r'/[^\x00-\x7F]|\?',
            r'retail\s/gi' # Remove "Retail"
            r'.\([0-9]+[a-z]{0,2}\)' # "Drink 100g (800g)" -> "Drink 100g"
        ]: name = re.sub(rgx, '', name)
        adapter['name'] = name

        safe_attrs = clean.defs.safe_attrs
        cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())

        nutrition_table = adapter.get('nutrition_table')[0]
        nutrition_table = cleaner.clean_html(nutrition_table)
        adapter['nutrition_table'] = nutrition_table

        product_info = adapter.get('product_info')[0]
        product_info = cleaner.clean_html(product_info)
        adapter['product_info'] = product_info

        print("     PORDUCT INFO !!!!!!!!!!!!!!!                 !!!!!!!!!!")
        print(product_info)

        img_small = adapter.get('img_small')[0]
        img_big = adapter.get('img_big')[0]

        if img_small:
            img_small = 'https://www.booker.co.uk' + img_small
            img_big = 'https://www.booker.co.uk' + img_big
        else:
            img_small = None
            img_big = None

        adapter['img_small'] = img_small
        adapter['img_big'] = img_big

        return item
