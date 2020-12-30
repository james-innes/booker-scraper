
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup, Comment
import re

class ProductPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        name = adapter.get('name')[0]
        for rgx in [
            r'/\?ÕÌ_|_Œ‚|[ŠŽÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÞßðÿ_]+',
            r'.PMP\s?£?(\d+.?\d+)',  # "PMP £3.29"
            r'(\d+)\s?x\s?',  # Remove "36 x "
            r'/[^\x00-\x7F]|\?',
            r'retail\s/gi', # Remove "Retail"
            r'.\([0-9]+[a-z]{0,2}\)' # "Drink 100g (800g)" -> "Drink 100g"
        ]: name = re.sub(rgx, '', name)
        adapter['name'] = name

        def remove_attrs(soup):
            for tag in soup.findAll(True): 
                tag.attrs = None
            return soup

        if adapter.get('nutrition_table'): 
            nutrition_table = adapter.get('nutrition_table')[0]
            soup = BeautifulSoup(nutrition_table, "html.parser")
            nutrition_table = remove_attrs(soup)
            adapter['nutrition_table'] = nutrition_table

        if 'product_info' in adapter:
            product_info = adapter.get('product_info')
            soup = BeautifulSoup(product_info, "html.parser")
            product_info = remove_attrs(soup)
            for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
                comment.extract()
            adapter['product_info'] = product_info
        else:
            adapter['product_info'] = None

        if "img_small" in adapter:
            img_small = 'https://www.booker.co.uk' + adapter.get('img_small')[0]
            adapter['img_small'] = img_small

        if "img_big" in adapter:
            img_big = 'https://www.booker.co.uk' + adapter.get('img_big')[0]
            adapter['img_big'] = img_big


        adapter['code'] = adapter['code'][0]

        return item
