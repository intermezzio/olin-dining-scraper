import random
import json
from dining import DiningInfoManager, all_days, weekdays, weekends
from scrape import get_image_any_format
import random_stuff as rs


class UrBadException(Exception):
    pass


class MessageGenerator:
    def __init__(self, json_file=None):
        if json_file:
            with open(json_file) as infile:
                self.menu = json.load(infile)
        else:
            self.dining_info_manager = DiningInfoManager()
            self.menu = self.dining_info_manager.menu
        self._load_assets()

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

        self.numbers = [str(i) for i in range(2, 21)]

    def generate_day_message(self, day, quotes=3):
        dinner_entree = self.menu[day]["Dinner"]["Entree"]
        get_image_any_format(dinner_entree)

        caption = f"Accurate depiction of {dinner_entree} in the dining hall"

        if day in weekdays:
            message_str = (
                "Breakfast:\n"
                + self.generate_message(day, "Breakfast", quotes=quotes)
                + "\nLunch:\n"
                + self.generate_message(day, "Lunch", quotes=quotes)
                + "\nDinner:\n"
                + self.generate_message(day, "Dinner", quotes=quotes)
            )
        else:
            message_str = (
                "No brunch info available.\n"
                + "\nDinner:\n"
                + self.generate_message(day, "Dinner", quotes=quotes)
            )

        return message_str, caption

    def generate_message(self, day, meal, quotes=1):
        message_str = ""
        items = [""]

        if day in weekdays:
            if meal == "Breakfast":
                message_str, items = self._generate_breakfast(day)
            elif meal == "Lunch":
                message_str, items = self._generate_lunch(day)
            elif meal == "Dinner":
                message_str, items = self._generate_weekday_dinner(day)
            else:
                raise UrBadException("Bad meal name, mere mortal!")
        elif day in weekends:
            if meal == "Brunch":
                message_str = "Tough luck this is brunch. \n"
                return message_str
            elif meal == "Dinner":
                message_str, items = self._generate_weekend_dinner(day)
            else:
                raise UrBadException("Bad meal name, mere mortal!")
        else:
            raise UrBadException("Bad day of the week, mere mortal!")

        if quotes:
            message_str += "\n" + self.meme_quotes(items, num=quotes)

        return message_str

    def _generate_weekday_dinner(self, day):
        dinner_details = self.menu[day]["Dinner"]
        dinner_entree = dinner_details["Entree"]
        main_dinner_items = list(
            filter(
                lambda x: x
                and x
                not in (
                    "Bistro Plates:",
                    "Simply Cooked",
                    "Burger Bar:",
                    "Daily Special",
                ),
                dinner_details["Grill"].split("\n"),
            )
        )
        pizza_items = list(
            filter(
                lambda x: x
                and "lunch only" not in x
                and x not in ("Pasta Bar:", "Specialty Sub"),
                dinner_details["Pizza"].split("\n"),
            )
        )

        message_str = "Today's main dinner entree is " + dinner_entree + "\n"

        message_str += "Main items:\n"
        for item in main_dinner_items:
            message_str += "+ " + item + "\n"

        message_str += "Pizzas and Pastas:\n"
        for item in pizza_items:
            message_str += "+ " + item + "\n"

        return (message_str, [dinner_entree] + main_dinner_items + pizza_items)

    def _generate_weekend_dinner(self, day):
        dinner_details = self.menu[day]["Dinner"]
        dinner_entree = dinner_details["Entree"]
        main_dinner_items = list(
            filter(
                lambda x: x
                and x
                not in (
                    "Bistro Plates:",
                    "Simply Cooked",
                    "Burger Bar:",
                    "Daily Special",
                ),
                dinner_details["Grill"].split("\n"),
            )
        )

        message_str = "Today's main dinner entree is " + dinner_entree + "\n"

        message_str += "Main items:\n"
        for item in main_dinner_items:
            message_str += "+ " + item + "\n"

        return (message_str, [dinner_entree] + main_dinner_items)

    def _generate_lunch(self, day):
        lunch_details = self.menu[day]["Lunch"]
        lunch_entree = lunch_details["Entree"]
        lunch_sandwich = lunch_details["Sandwiches"]
        main_lunch_items = list(
            filter(
                lambda x: x
                and x
                not in (
                    "Bistro Plates:",
                    "Simply Cooked",
                    "Burger Bar:",
                    "Daily Special",
                ),
                lunch_details["Grill"].split("\n"),
            )
        )
        pizza_items = list(
            filter(
                lambda x: x and x not in ("Pasta Bar:", "Specialty Sub"),
                lunch_details["Pizza"].split("\n"),
            )
        )

        message_str = "Today's main lunch entree is " + lunch_entree + "\n"
        message_str += "That section on the right has " + lunch_sandwich + "\n"

        message_str += "Main items:\n"
        for item in main_lunch_items:
            message_str += "+ " + item + "\n"

        message_str += "Pizzas and Pastas:\n"
        for item in pizza_items:
            message_str += "+ " + item + "\n"

        return (
            message_str,
            [lunch_entree, lunch_sandwich] + main_lunch_items + pizza_items,
        )

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
                sandwich = breakfast_items[i + 1]
            elif item == "Egg of the Day":
                skip = True
                egg = breakfast_items[i + 1]
            else:
                main_breakfast_items.append(item)

        message_str = "Today's breakfast includes:\n"
        for item in main_breakfast_items:
            message_str += "+ " + item + "\n"

        message_str += "Sandwich: " + sandwich + "\n"
        message_str += "Egg:      " + egg + "\n"
        return (message_str, main_breakfast_items + [sandwich] + [egg])

    def meme_quotes(self, items, num=1):
        all_comments = []

        if num < len(self.comments):
            comments = random.sample(self.comments, num)
        else:
            comments = random.choices(self.comments, k=num)

        if num < len(items):
            selected_items = random.sample(items, num)
        else:
            selected_items = random.choices(items, k=num)

        if num < len(self.adjectives):
            adjs = random.sample(self.adjectives, num)
        else:
            adjs = random.choices(self.adjectives, k=num)

        if num < len(self.eat):
            eats = random.sample(self.eat, num)
        else:
            eats = random.choices(self.eat, k=num)

        if num < len(self.classes):
            classes = random.sample(self.classes, num)
        else:
            classes = random.choices(self.classes, k=num)

        if num < len(self.names):
            names = random.sample(self.names, num)
        else:
            names = random.choices(self.names, k=num)

        nums = random.choices(self.numbers, k=num)

        for comment, item, adj, eat, class_, num, name in zip(
            comments, selected_items, adjs, eats, classes, nums, names
        ):
            comment = comment.replace(r"{item}", item)
            comment = comment.replace(r"{adj}", adj)
            comment = comment.replace(r"{eat}", eat)
            comment = comment.replace(r"{class}", class_)
            comment = comment.replace(r"{num}", num)
            comment = f'"{comment}"\n\t- {name}\n'
            all_comments.append(comment)

        return "\n".join(all_comments)

    def generate_meme_message(self, day, meal):
        pass

    def send_message(self, message):
        pass


if __name__ == "__main__":
    m = MessageGenerator()
