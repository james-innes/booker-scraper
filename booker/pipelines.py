
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup, Comment
import re

class ProductPipeline:
	def process_item(self, item, spider):
		adapter = ItemAdapter(item)

		def clean_image(image):
			image = re.sub(r'\/bbimages', '', image)
			return image
				
		def clean_name(name):
			for rgx in [
				r'/\?ÕÌ_|_Œ‚|[ŠŽÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÞßðÿ_]+',
				r'.PMP\s?£?(\d+.?\d+)', # PMP £3.29
				r'(\d+)\s?x\s?', # 36 x
				r'/[^\x00-\x7F]|\?',
				r'retail\s/gi', # Retail
				r'.\([0-9]+[a-z]{0,2}\)' # "Drink 100g (800g)" -> "Drink 100g"
			]: name = re.sub(rgx, '', name.lstrip())
			return name

		def clean_value(value):
			for rgx in [
				r'[£%]',
				r'POR: ',
				r'RRP: ',
				r'Case of '
			]: value = re.sub(rgx, '', value)
			return value

		def clean_html(html):
			for rgx in [
				r'\ {2,}',
			]: html = re.sub(rgx, '', str(html))

			soup = BeautifulSoup(html, "html.parser")
			for tag in soup.findAll(True): tag.attrs = None
			for comment in soup.findAll(text=lambda text:isinstance(text, Comment)): comment.extract()

			soup = re.sub(r'span>By ', 'span>', str(soup))
			soup = re.sub(r'(<br\/>){1,}', '<br />', str(soup))
			return soup
		

		if spider.name == "product_list":
			adapter['img_small'] = clean_image(adapter.get('img_small')[0])
			if adapter.get('por'): adapter['por'] = clean_value(adapter.get('por')[0])
			if adapter.get('rrp'): adapter['rrp'] = clean_value(adapter.get('rrp')[0])
			if adapter.get('case'): adapter['case'] = clean_value(adapter.get('case')[0])
			adapter['wsp_inc_vat'] = clean_value(adapter.get('wsp_inc_vat')[0])

		if spider.name == "product_detail":
			adapter['name'] = clean_name(adapter.get('name'))
			adapter['code'] = adapter.get('code')[0]
			adapter['img_big'] = clean_image(adapter.get('img_big')[0])
			adapter['info'] = clean_html(adapter.get('info'))

		return item


