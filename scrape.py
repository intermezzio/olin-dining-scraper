import shutil
import requests
import random
import re
from duckduckgo_search import ddg_images

fixer = re.compile(r'<[^>]+>')

def get_image(search_term):
	global fixer
	search_term = fixer.sub('', search_term)
	image_search = ddg_images(search_term + " png", safesearch="On", max_results=10)
	if not image_search:
		return ""
	image = random.choice(image_search[:10])
	image_url = image["image"]
	response = requests.get(image_url, stream=True)
	with open("featured_img.png", "wb") as outfile:
		shutil.copyfileobj(response.raw, outfile)
	del response