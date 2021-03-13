import os
import sys
import csv
from urllib import error
from urllib import request
from PIL import Image
from io import BytesIO


def download_image(key, url):
		filename = '{}.jpg'.format(key)

		if os.path.exists(filename):
				print('Image {} already exists. Skipping download.'.format(filename))
				return 0

		try:
				response = request.urlopen(url)
				image_data = response.read()
		except:
				print('Warning: Could not download image {} from {}'.format(key, url))
				writer.writerow(
						{
								'error': "download",
								"filename": filename,
								'key': key,
								"url": url
						}
				)

				return 1

		try:
				pil_image = Image.open(BytesIO(image_data))
		except:
				print('Warning: Failed to parse image {}'.format(key))
				writer.writerow(
						{
								'error': "parse",
								"filename": filename,
								'key': key,
								"url": url
						}
				)
				return 1

		try:
				pil_image_rgb = pil_image.convert('RGB')
		except:
				print('Warning: Failed to convert image {} to RGB'.format(key))
				writer.writerow(
						{
								'error': "convert",
								"filename": filename,
								'key': key,
								"url": url
						}
				)
				return 1

		try:
				pil_image_rgb.save(filename, format='JPEG', quality=90)
		except:
				print('Warning: Failed to save image {}'.format(filename))
				writer.writerow(
						{
								'error': "save",
								"filename": filename,
								'key': key,
								"url": url
						}
				)
				return 1

		return 0


csvfile = open("image.csv", 'r')
csvreader = csv.reader(csvfile)
key_url_list = [line[:2] for line in csvreader]
key_url_list = key_url_list[1:]

with open('logs.csv', 'w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=['error', 'key', 'url', 'filename'])
		writer.writeheader()

		for key, url in key_url_list:
				download_image(key, url)
