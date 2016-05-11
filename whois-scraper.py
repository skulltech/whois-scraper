from lxml import html
from PIL import Image
import requests
import urllib.request

def enlarge_image(image_file):
	image = Image.open(image_file)
	enlarged_size = map(lambda x: x*2, image.size)
	enlarged_image = image.resize(enlarged_size)

	return enlarged_image

def extract_text(image_file):
	image = enlarge_image(image_file)

	# Use Tesseract to extract text from the enlarged image. Then Return it.

def fix_emails(whois_data, image_urls):
	count = 0

	for index, item in enumerate(whois_data):
		if item.startswith('@'):
			with urllib.request.urlopen(image_urls[count]) as response:
				email_username = extract_text(response)
			
			whois_data[index-1:index+1] = [whois_data[index-1] + email_username + whois_data[index]]
			count += 1

	return whois_data

def scrape_whois(domain):
	domain = 'speedtest.net'

	page = requests.get('http://www.whois.com/whois/{}'.format(domain))
	tree = html.fromstring(page.content)

	registrar_data = tree.xpath('//*[@id="registrarData"]/text()')
	registrar_images = list(map(lambda x: 'http://www.whois.com' + x, tree.xpath('//*[@id="registrarData"]/img/@src')))
	registry_data = tree.xpath('//*[@id="registryData"]/text()')
	registry_images = list(map(lambda x: 'http://www.whois.com' + x, tree.xpath('//*[@id="registryData"]/img/@src')))