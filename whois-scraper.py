from lxml import html
from PIL import Image
import requests
import urllib.request
import csv
from io import BytesIO
import time

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
	page = requests.get('http://www.whois.com/whois/{}'.format(domain))
	tree = html.fromstring(page.content)

	registrar_data = tree.xpath('//*[@id="registrarData"]/text()')
	registrar_images = list(map(lambda x: 'http://www.whois.com' + x, tree.xpath('//*[@id="registrarData"]/img/@src')))
	registry_data = tree.xpath('//*[@id="registryData"]/text()')
	registry_images = list(map(lambda x: 'http://www.whois.com' + x, tree.xpath('//*[@id="registryData"]/img/@src')))

	for x, n in enumerate(registrar_images):
		im = Image.open(BytesIO(requests.get(n).content))
		im.save('{domain}-{index}.png'.format(domain=domain, index=x))
	
	return [registry_data, registrar_data]

file_name = 'Book1.csv'


with open(file_name, newline='') as input_csv:
    csv_reader = csv.reader(input_csv)

    with open('whois_data.csv', mode='w', newline='') as output_csv:
        csv_writer = csv.writer(output_csv)
        for row in csv_reader:
            ret = scrape_whois(row[0])
            csv_writer.writerow([row[0], '|'.join(ret[0]), '|'.join(ret[1])])
            time.sleep(2)