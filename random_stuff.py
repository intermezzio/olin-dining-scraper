import json
import random
import requests
import string
from icecream import ic

def get_address(n=1):
	return get_item("address", lambda x: x["full_address"], n=n)

def get_appliance(n=1):
	return get_item("appliance", lambda x: x["equipment"], n=n)

def get_avatar(n=1):
	return [
		f"https://api.minimalavatars.com/avatar/{get_string(8)}/png"
		for _ in range(n)
	]

def get_beer_brand(n=1):
	return get_item("beer", lambda x: x["brand"], n=n)

def get_capital(n=1):
	return get_item("nation", lambda x: x["capital"], n=n)		

def get_car(n=1):
	return get_item("vehicle", lambda x: x["color"] + " " + x["make_and_model"], n=n)

def get_country(n=1):
	return get_item("address", lambda x: x["country"], n=n)

def get_credit_card(n=1):
	return get_item("users", lambda x: x["credit_card"]["cc_number"], n=n, suffix="user")

def get_food(n=1):
	return get_item("food", lambda x: x["dish"], n=n)

def get_food_long(n=1):
	return get_item("food", lambda x: x["dish"] + " with " + x["measurement"] + " " + x["ingredient"], n=n)

def get_hipster(n=1):
	return get_item("hipster", lambda x: x["word"], n=n, suffix="hipster_stuff")

def get_ingredient(n=1):
	return get_item("food", lambda x: x["ingredient"], n=n)

def get_ip_addr(n=1):
	return get_item("internet_stuff", lambda x: x["ip_v4_address"], n=n)

def get_language(n=1):
	return get_item("nation", lambda x: x["language"], n=n)

def get_name(n=1):
	return get_item("users", lambda x: x["first_name"] + " " + x["last_name"], n=n, suffix="user")

def get_nationality(n=1):
	return get_item("nation", lambda x: x["nationality"], n=n)

def get_number(n=1):
	return [str(x) for x in random.choices(list(range(2,21)), k=n)]

def get_phone_number(n=1):
	return get_item("users", lambda x: x["phone_number"], n=n, suffix="user")

def get_ssn(n=1):
	return get_item("id_number", lambda x: x["valid_us_ssn"], n=n)

def get_string(n=1):
	return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

def get_item(name, parser, n=5, suffix=None):
	url = f"https://random-data-api.com/api/{name}/random_{suffix if suffix else name}"

	response = requests.get(url, params={"size": n})
	pythonic_response = response.json()
	list_output = list(map(parser, pythonic_response))

	return list_output


if __name__ == "__main__":
	x = get_food()