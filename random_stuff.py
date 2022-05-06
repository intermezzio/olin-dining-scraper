import json
import requests
from icecream import ic

def get_foods(n=5, ingredient=True):
	if ingredient:
		parser = lambda x: x["dish"] + " with " + x["measurement"] + " " + x["ingredient"]
	else:
		parser = lambda x: x["dish"]

	return get_item("food", parser, n=n)

def get_hipster(n=1):
	return get_item("hipster", lambda x: x["word"], n=n)

def get_address(n=1):
	return get_item("address", lambda x: x["full_address"], n=n)

def get_country(n=1):
	return get_item("address", lambda x: x["country"], n=n)

def get_capital(n=1):
	return get_item("nation", lambda x: x["capital"], n=n)		

def get_appliance(n=1):
	return get_item("appliance", lambda x: x["equipment"], n=n)

def get_beer_brand(n=1):
	return get_item("beer", lambda x: x["brand"], n=n)

def get_item(name, parser, n=5):
	url = f"https://random-data-api.com/api/{name}/random_{name}"
	if name == "hipster": # workaround
		url += "_stuff"

	response = ic(requests.get(url, params={"size": n}))
	pythonic_response = ic(response.json())
	list_output = list(map(parser, pythonic_response))

	return list_output


if __name__ == "__main__":
	x = get_foods()