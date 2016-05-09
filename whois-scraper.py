from lxml import html
from PIL import Image
import requests

def enlarge_image(image_file):
	image = Image.open(image_file)
	enlarged_size = map(lambda x: x*2, image.size)
	enlarged_image = image.resize(enlarged_size)

	return enlarged_image

def extract_text(image_file):
	image = enlarge_image(image_file)

	# Use Tesseract to extract text from the enlarged image. Then Return it.

domain = 'speedtest.net'

page = requests.get('http://www.whois.com/whois/{}'.format(domain))
tree = html.fromstring(page.content)
