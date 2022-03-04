from dining import DiningInfoManager, all_days, weekdays, weekends
import random
import json

class MessageGenerator:
	def __init__(self, json_file=None):
		if json_file:
			with open(json_file) as infile:
				self.menu = json.load(infile)
		else:
			self.dining_info_manager = DiningInfoManager()
			self.menu = self.dining_info_manager.menu
		self._load_assets()

	@staticmethod
	def from_json(cls, json_file):
		pass

	def _load_assets(self):
		with open("assets/adjectives.txt") as infile:
			self.adjectives = infile.read().strip().split("\n")

		with open("assets/classes.txt") as infile:
			self.classes = infile.read().strip().split("\n")
		
		with open("assets/comments.txt") as infile:
			self.comments = infile.read().strip().split("\n")
		
		with open("assets/eat.txt") as infile:
			self.eat = infile.read().strip().split("\n")

		with open("assets/names.txt") as infile:
			self.names = infile.read().strip().split("\n")

		self.numbers = [str(i) for i in range(2,21)]
		
		
	def generate_message(self, day, meal, quote=True):
		message_str = ""
		items = [""]

		if day in weekdays:
			if meal == "Breakfast":
				message_str, items = self._generate_breakfast(day)
			elif meal == "Lunch":
				message_str, items = self._generate_lunch(day)

		if quote:
			message_str = self.meme_quote(items)

		return message_str

	def _generate_lunch(self, day):
		lunch_details = self.menu[day]["Lunch"]
		lunch_entree = lunch_details["Entree"]
		lunch_sandwich = lunch_details["Sandwiches"]
		main_lunch_items = list(filter(
			lambda x: x and x not in ("Bistro Plates:", "Simply Cooked", "Burger Bar:", "Daily Special"),
			lunch_details["Grill"].split("\n")
		))
		pizza_items = list(filter(
			lambda x: x and x not in ("Pasta Bar:", "Specialty Sub"),
			lunch_details["Pizza"].split("\n")
		))
		
		message_str = "Today's main lunch entree is " + lunch_entree + "\n"
		message_str += "That section on the right has " + lunch_sandwich + "\n"

		message_str += "Main items:\n"
		for item in main_lunch_items:
			message_str += "+ " + item + "\n"

		message_str += "Pizzas and Pastas:\n"
		for item in pizza_items:
			message_str += "+ " + item + "\n"

		return (message_str, [lunch_entree, lunch_sandwich] + main_lunch_items + pizza_items)


	def _generate_breakfast(self, day):
		breakfast_items = self.menu[day]["Breakfast"].split("\n")
		main_breakfast_items = list()
		sandwich = ""
		egg = ""

		skip = False
		for i, item in enumerate(breakfast_items):
			if skip:
				skip = False
				continue
			if item == "Breakfast Sandwich of the Day":
				skip = True
				sandwich = breakfast_items[i+1]
			elif item == "Egg of the Day":
				skip = True
				egg = breakfast_items[i+1]
			else:
				main_breakfast_items.append(item)

		message_str = "Today's breakfast includes:\n"
		for item in main_breakfast_items:
			message_str += "+ " + item + "\n"

		message_str += "Sandwich: " + sandwich + "\n"
		message_str += "Egg:      " + egg
		return (message_str, main_breakfast_items + [sandwich] + [egg])

	def meme_quote(self, items):
		comment = random.choice(self.comments)
		comment = comment.replace(r"{item}", random.choice(items))
		comment = comment.replace(r"{adj}", random.choice(self.adjectives))
		comment = comment.replace(r"{eat}", random.choice(self.eat))
		comment = comment.replace(r"{class}", random.choice(self.classes))
		comment = comment.replace(r"{num}", random.choice(self.numbers))

		comment = "\"" + comment + "\"\n\t- " + random.choice(self.names)
		return comment

	def generate_meme_message(self, day, meal):
		pass

	def send_message(self, message):
		pass

if __name__ == "__main__":
	m = MessageGenerator()
	