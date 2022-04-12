import shutil
import requests
from duckduckgo_search import ddg_images

def get_image(search_term):
	image_search = ddg_images(search_term + " png", safesearch="On", max_results=10)
	if not image_search:
		return ""
	image_url = image_search[0]["image"]
	response = requests.get(image_url, stream=True)
	with open("featured_img.png", "wb") as outfile:
		shutil.copyfileobj(response.raw, outfile)
	del response