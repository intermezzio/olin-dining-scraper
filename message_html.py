from bs4 import BeautifulSoup
from icecream import ic
from scrape import get_image
from quotes import Quotes
import random_stuff as rs
import itertools
import copy
from dining import DiningInfoManager, all_days, weekdays, weekends
from send import send_mail, email_recipients, debug_email, email_bot


class MessageGenerator:
    def __init__(self):
        """
        Create a BeautifulSoup object based on a template
        and edit the html so that it has the content
        it needs, then send the html in an email
        """
        with open("assets/template.html") as infile:
            self.template = BeautifulSoup(infile, "lxml")

        self.quotes = Quotes()

    def __str__(self):
        return str(self.template)

    def export(self, to="assets/output.html"):
        with open(to, "w") as outfile:
            outfile.write(str(self.template))

    def send(self):
        send_mail(debug_email, subject="NOT Dining Hall Food", body=str(self.template))

    @classmethod
    def from_template(cls, menu_dict, day = "Monday"):
        """
        {"breakfast": [items], "lunch": [items], "dinner": [items]}
        """
        ic(menu_dict)
        mg = cls()

        entree = menu_dict["dinner"][0]
        mg.set_entree(entree)
        mg.set_marketing(entree)

        for meal, items in menu_dict.items():
            # mg._create_meal(meal)
            mg._set_meal(items, meal)
            mg._set_meal_comments(items, meal)
        
        if day in weekends:
            # delete breakfast and lunch
            mg.template.find(id="breakfast").extract()
            mg.template.find(id="lunch").extract()

        return mg

    def _create_meal(self, meal):
        if meal == "dinner":
            return
        
        dinner_section = self.template.find(id="dinner").copy()
        meal_section = dinner_section.copy()
        meal_comments_section = self.template.find(id="dinner-comments").copy()

        meal_section['id'] = meal
        meal_comments_section['id'] = f"{meal}-comments"

        dinner_section.insert_before(meal_comments_section)
        meal_comments_section.insert_before(meal_section)
		

    @classmethod
    def from_dh(cls, manager, day):
        """
        Generate an HTML template from the dining hall scraper output
        """
        ic(manager.menu)
        if day in weekdays:
            breakfast_items = list(
                filter(
                    lambda x: "of the Day" not in x,
                    manager.menu[day]["Breakfast"].split("\n"),
                )
            )

            lunch_items = list()
            lunch_dict = manager.menu[day]["Lunch"]
            for key in ("Sandwiches", "Entree", "Grill", "Pizza"):
                lunch_items += lunch_dict.pop(key, "").split("\n")
        else:
            breakfast_items = list()
            lunch_items = list()

        
        dinner_items = list()
        dinner_dict = manager.menu[day]["Dinner"]
        for key in ("Entree", "Grill", "Pizza"):
            dinner_items += dinner_dict.pop(key, "").split("\n")

        template_dict = {
            "breakfast": breakfast_items,
            "lunch": lunch_items,
            "dinner": dinner_items,
        }

        return cls.from_template(template_dict, day)

    def set_entree(self, entree):
        main_entree_text = self.template.find(id="main-dinner-entree")
        main_entree_text.string.replace_with(entree)

        image_url = get_image(rs.get_food()[0], url_only=True)
        main_entree_bg = self.template.find(id="background-dinner-entree")
        self._change_bg_image(main_entree_bg, image_url)

    def set_marketing(self, entree):
        marketing_text = self.template.find(id="marketing")
        marketing_text.string.replace_with(f"Inaccurate depiction of {entree}")

        marketing_description_text = self.quotes.get_marketing()[0]
        marketing_description = self.template.find(id="marketing-description")
        marketing_description.string.replace_with(marketing_description_text)

    def set_breakfast(self, meal_items):
        self._set_meal(meal_items, meal="breakfast")

    def set_breakfast_comments(self, meal_items):
        self._set_meal_comments(meal_items, "breakfast")

    def set_lunch(self, meal_items):
        self._set_meal(meal_items, meal="lunch")

    def set_lunch_comments(self, meal_items):
        self._set_meal_comments(meal_items, "lunch")

    def set_dinner(self, meal_items):
        self._set_meal(meal_items, meal="dinner")

    def set_dinner_comments(self, meal_items):
        self._set_meal_comments(meal_items, "dinner")

    def _set_meal(self, meal_items, meal="breakfast"):
        meal_table = self.template.find(id=f"{meal}-items")  # <table>
        mt_left, mt_right = meal_table.find_all("table")
        sample_tr = copy.copy(mt_left.find("tr"))

        for tag in mt_left.find_all("tr") + mt_right.find_all("tr"):
            tag.clear()

        for item, mt in zip(meal_items, itertools.cycle((mt_left, mt_right))):
            this_tr = copy.copy(sample_tr)

            # image_url = get_image(item, url_only=True)
            descriptor = self.quotes.get_adjective()[0]

            this_tr.select("h3 > a")[0].string.replace_with(item)
            this_tr.find(class_="price").string.replace_with(descriptor)
            # this_tr.find("img")["src"] = image_url

            mt.append(this_tr)

    def _set_meal_comments(self, meal_items, meal="breakfast"):
        meal_comments = self.quotes.get_quotes(meal_items, n=2, quote_only=True)

        parent_node = self.template.find(id=f"{meal}-comments")

        for comment, name, img_node, name_node, comment_node in zip(
            meal_comments,
            self.quotes.get_name(n=2),
            parent_node.find_all("img"),
            parent_node.find_all(class_="name"),
            parent_node.select(".text-testimony > p"),
        ):
            img_node["src"] = rs.get_avatar()[0]
            name_node.string.replace_with(self.quotes.get_name()[0])
            comment_node.string.replace_with(comment)

    def _change_bg_image(self, node, url):
        node["style"] = node["style"].replace("/*image*/", url)


if __name__ == "__main__":
    mg = MessageGenerator.from_template(
        {
            "breakfast": ["Eggs", "Tater Tots", "Homefries", "Tofu Scramble"],
            "lunch": [
                "BYO Deli Sandwiches",
                "Veggie Burger",
                "White Broccoli Garlic Pizza",
            ],
            "dinner": [
                "New England",
                "Baked Potato Bar",
                "Tomato Mozzarella Flatbread",
                "Ham",
            ],
        }
    )
    # mg.set_entree("Mongolian Beef")
    # mg.set_breakfast(["Eggs", "Ham", "Milk and cereal", "Gritz", "Breakfast pizza", "Orange Juice"])
    # mg.set_breakfast_comments(["Eggs", "Ham", "Milk and cereal", "Gritz", "Breakfast pizza", "Orange Juice"])
    mg.export()
