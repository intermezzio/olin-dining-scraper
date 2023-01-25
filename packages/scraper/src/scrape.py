import shutil
import requests
import random
import re
import os
import subprocess
from duckduckgo_search import ddg_images
import urllib.request
import io
from icecream import ic

fixer = re.compile(r"<[^>]+>")


def get_image(search_term, url_only=False):
    global fixer
    search_term = fixer.sub("", search_term)
    try:
        image_search = ddg_images(search_term, safesearch="On", max_results=100)
    except Exception:
        image_search = None
    if not image_search:
        return "https://lifestyleasia.onemega.com/wp-content/uploads/2018/04/The-Disney-movie-made-the-traditional-French-dish-Ratatouille-world-famous.png"

    random.shuffle(image_search)  # randomize output

    for image in image_search:  # random.choice(image_search[:10])
        image_url = image["image"]

        try:
            path = urllib.request.urlopen(ic(image_url))
            meta = path.info()
            image_size = int(meta.get(name="Content-Length"))
            if ic(image_size) > 5 * 1e6:  # if over 5MB
                ic("file too big")

                continue
        except:
            continue

        if image_url[-4:] == ".png" or url_only:
            break
    else:
        # ratatouille
        image_url = "https://lifestyleasia.onemega.com/wp-content/uploads/2018/04/The-Disney-movie-made-the-traditional-French-dish-Ratatouille-world-famous.png"

    if url_only:
        return image_url

    response = requests.get(image_url, stream=True)
    with open("featured_img.png", "wb") as outfile:
        shutil.copyfileobj(response.raw, outfile)


def get_image_any_format(search_term):
    global fixer
    search_term = fixer.sub("", search_term)
    image_search = ddg_images(search_term, safesearch="On", max_results=100)

    random.shuffle(image_search)  # randomize output

    if not image_search:
        return

    os.system("mkdir -p cache/")
    os.system("rm -f cache/*")

    for image in image_search:  # random.choice(image_search[:10])
        image_url = image["image"]

        first_filename = "cache/" + image_url.split("/")[-1]
        response = requests.get(image_url, stream=True)
        with open(first_filename, "wb") as outfile:
            shutil.copyfileobj(response.raw, outfile)

        try:
            txt = subprocess.check_output(
                ["convert", first_filename, "featured_img.png"]
            )
            print(txt)
            if txt == b"":
                break
        except subprocess.CalledProcessError as err:
            print(err)

        os.system(f'rm "{first_filename}"')
    else:
        print("Fallback to png")
        get_image(search_term)

    os.system(f'rm "{first_filename}"')
