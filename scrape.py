from bs4 import BeautifulSoup
import requests
import json
from icecream import ic

URL = "https://rebeccasculinarygroup.com/olin/menu-items/"

weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")

class DiningInfoManager:
	def __init__(self):
		self._get_details()

	def _get_details(self):
		self.webpage = requests.get(URL)
		self.soup = BeautifulSoup(self.webpage.content, "lxml")
		self.all_details = self.soup.find_all(class_="tabDetails")

	def get_info(self, day, meal):
		pass

	def get_breakfasts(self):
		breakfast_info = self.all_details[0]
		node = breakfast_info.find("span")
		assert node.text == "Breakfast"

		self.breakfast_dict = dict()

		weekday_index = 0
		weekday = ic(weekdays[weekday_index])
		for node in breakfast_info.find_all(recursive=False):
			if weekday in node.text:
				self.breakfast_dict[weekday] = ""
				weekday_index += 1
				weekday = ic(weekdays[weekday_index]) if weekday_index < len(weekdays) else "Saturday"
			elif ic(weekday_index) >= 1:
				self.breakfast_dict[weekdays[ic(weekday_index-1)]] += str(node.text) + "\n"
			node = ic(node.find_next())
		return self.breakfast_dict

if __name__ == "__main__":
	d = DiningInfoManager()
	breakfasts = d.get_breakfasts()
	print(breakfasts)
	with open("breakfast.txt", "w") as outfile:
		json.dump(breakfasts, outfile, indent=4)