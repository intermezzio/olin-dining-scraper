import shutil
import requests
import random
import re
import os
import subprocess
from duckduckgo_search import ddg_images

fixer = re.compile(r'<[^>]+>')

def get_image(search_term):
	global fixer
	search_term = fixer.sub('', search_term)
	image_search = ddg_images(search_term + " png", safesearch="On", max_results=10)
	if not image_search:
		return
	image = image_search[0] # random.choice(image_search[:10])
	image_url = image["image"]
	response = requests.get(image_url, stream=True)
	with open("featured_img.png", "wb") as outfile:
		shutil.copyfileobj(response.raw, outfile)

def get_image_any_format(search_term):
	global fixer
	search_term = fixer.sub('', search_term)
	image_search = ddg_images(search_term, safesearch="On", max_results=100)

	random.shuffle(image_search) # randomize output

	if not image_search:
		return

	os.system("mkdir -p cache/")
	os.system("rm -f cache/*")

	for image in image_search: # random.choice(image_search[:10])
		image_url = image["image"]
		
		first_filename = "cache/" + image_url.split("/")[-1]
		response = requests.get(image_url, stream=True)
		with open(first_filename, "wb") as outfile:
			shutil.copyfileobj(response.raw, outfile)

		try:
			txt = subprocess.check_output(["convert", first_filename, "featured_img.png"])
			print(txt)
			if txt == b'':
				break
		except subprocess.CalledProcessError as err:
			print(err)
		
		os.system(f"rm \"{first_filename}\"")		
	else:
		print("Fallback to png")
		get_image(search_term)

	os.system(f"rm \"{first_filename}\"")

