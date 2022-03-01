from bs4 import BeautifulSoup
import requests
import json
from icecream import ic

URL = "https://rebeccasculinarygroup.com/olin/menu-items/"

all_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
weekdays = all_days[:5]

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
		self.breakfast_dict = self._get_section(breakfast_info,
			weekdays, "Breakfast")
		return self.breakfast_dict

	def get_lunch_specials(self):
		lunch_specials_info = self.all_details[2]
		at_specials_section = False
		current_days_in_header = set()
		self.lunch_specials_dict = {day: "" for day in all_days}

		for node in lunch_specials_info.find_all(recursive=False):
			if not at_specials_section:
				if "Lunch Specials" in node.text:
					at_specials_section = True
				else:
					continue
			potential_days_in_header = set()
			for day in all_days:
				if day in node.text:
					potential_days_in_header.add(day)

			print(potential_days_in_header)
			if potential_days_in_header:
				current_days_in_header = potential_days_in_header
				continue
			
			for day in current_days_in_header:
				self.lunch_specials_dict[day] += str(node.text) + "\n"

		return self.lunch_specials_dict

	def get_entrees(self):
		entrees_info = self.all_details[3]
		self.lunch_entree_dict = self._get_section(entrees_info,
			weekdays, "Lunch", "Saturday")
		self.dinner_entree_dict = self._get_section(entrees_info,
			all_days, "Dinner")
		return (self.lunch_entree_dict, self.dinner_entree_dict)

	def get_grill(self):
		grill_info = self.all_details[4]
		self.lunch_grill_dict = self._get_section(grill_info,
			weekdays, "Lunch", "Dinner")
		self.dinner_grill_dict = self._get_section(grill_info,
			all_days, "Dinner")
		return (self.lunch_grill_dict, self.dinner_grill_dict)

	def get_pizza(self):
		pizza_info = self.all_details[5]
		self.pizza_dict = self._get_section(pizza_info,
			weekdays, "Available")
		return self.pizza_dict

	def _get_section(self, subsoup, dotw, start_str=None, end_str=None):
		has_started = start_str is None
		self.section_dict = {day: "" for day in dotw}

		dotw_index = 0
		day = dotw[dotw_index]
		for node in subsoup.find_all(recursive=False):
			if not has_started:
				if start_str in node.text:
					has_started = True
				else:
					continue
			if end_str and end_str in node.text:
				break

			if day in node.text:
				dotw_index += 1
				day = dotw[dotw_index] if dotw_index < len(dotw) else "Monday"
			elif dotw_index >= 1:
				self.section_dict[dotw[dotw_index-1]] += str(node.text) + "\n"
			node = node.find_next()
		return self.section_dict



if __name__ == "__main__":
	d = DiningInfoManager()
	# lunch_specials = d.get_lunch_specials()
	# print(lunch_specials)
	# with open("lunch_specials.txt", "w") as outfile:
	# 	json.dump(lunch_specials, outfile, indent=4)

	entrees = d.get_entrees()
	print(entrees)
	with open("entrees.txt", "w") as outfile:
		json.dump(entrees, outfile, indent=4)