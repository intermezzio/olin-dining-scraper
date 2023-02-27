from bs4 import BeautifulSoup
import requests
import json
import re
import string
from icecream import ic
import unicodedata
from tree import Tree
from functools import reduce
from operator import add

URL = "https://rebeccasculinarygroup.com/olin/menu-items/"

all_days = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)
weekdays = all_days[:5]
weekends = all_days[5:]


class DiningInfoManager:
    def __init__(self):
        self._fetch_site_data()

        self.menu = {
            day: {meal: {} for meal in ("Breakfast", "Lunch", "Dinner")}
            for day in weekdays
        } | {day: {meal: {} for meal in ("Lunch", "Dinner")} for day in weekends}

    def _fetch_site_data(self):
        self.webpage = requests.get(URL)
        self.soup = BeautifulSoup(self.webpage.content, "lxml")
        # with open("assets/site.html", "r") as infile:
        #     self.soup = BeautifulSoup(infile.read(), "lxml")
        self.all_details = self.soup.find_all(class_="tabDetails")
        
        self.all_text: list[list[str]] = []

        for panel in self.all_details:
            text = panel.get_text()
            text = unicodedata.normalize("NFKD", text)
            text = re.sub(r"\*\*\*", "", text)
            text = re.sub(r"Â", "", text)
            text = re.sub(r"\s*\n\s*", "\n", text)
            self.all_text.append(text.strip().split("\n"))
        
    def parse_menu(self):
        self._get_breakfasts()
        self._get_entrees()
        self._get_grill()
        self._get_pizza()

        with open("menu.json", "w") as outfile:
            json.dump(self.menu, outfile, indent=4)

    @staticmethod
    def _clean_str(input_str):
        printable = set(string.printable)
        output_str = "".join(filter(lambda x: x in printable, input_str)).strip()
        return output_str

    def get_items(self, day: str, meal: str) -> list[str]:
        base = self.menu[day][meal]
        return DiningInfoManager.extract(base)
    
    @staticmethod
    def extract(base) -> list[str]:
        if isinstance(base, list):
            return base
        elif isinstance(base, str):
            return [base]
        elif isinstance(base, dict):
            return reduce(add, (DiningInfoManager.extract(x) for _, x in base.items()))
        else:
            return []

    def _get_breakfasts(self) -> None:
        breakfast_info = self.all_text[0]

        def breakfast_hier(line: str) -> int:
            if line == "Breakfast":
                return -1
            elif line in all_days:
                return 1
            elif line == "Egg of the Day":
                return -1
            else:
                return 2
        
        self.breakfast_tree = Tree.from_list(breakfast_info, breakfast_hier)
        breakfast_dict = self.breakfast_tree.to_dict()
        for day, items in breakfast_dict["root"].items():  # type: ignore
            self.menu[day]["Breakfast"] = items  # type: ignore

    def _get_entrees(self):
        entrees_info = self.all_text[3]

        for i, line in enumerate(entrees_info):
            entrees_info[i] = line.replace(" (DR Independence Day)", "")

        def entrees_hier(line: str) -> int:
            if line == "Entree":
                return -1
            elif line.split()[0] in all_days:
                return 1
            elif line.lower() in ("lunch", "brunch", "dinner"):
                return 2
            elif line[0] == "(" and line[-1] == ")":
                return -1
            else:
                return 3
        
        entrees_tree = Tree.from_list(entrees_info, entrees_hier)
        entrees_dict = ic(entrees_tree.to_dict()["root"])  # type: ignore

        for day in entrees_dict.keys():  # type: ignore
            for meal, entrees in entrees_dict[day].items():
                if meal == "BRUNCH":
                    meal = "LUNCH"
                
                meal = meal[0] + meal[1:].lower()
                
                self.menu[day][meal]["Entree"] = entrees[0]

    def _get_grill(self):
        grill_info = self.all_text[4]
        
        def grill_hier(line: str) -> int:
            ic(line)
            if line in ("Grill", "Lunch Grill Items"):
                return -1
            elif line in ("Daily Special", "Simply Cooked", "Bistro Plate"):
                return -1
            elif line in all_days:
                return 1
            elif line.lower() in ("lunch", "brunch", "dinner"):
                return 2
            else:
                return 3
        
        grill_tree = Tree.from_list(grill_info, grill_hier)
        grill_dict = grill_tree.to_dict()["root"]  # type: ignore

        for day in grill_dict.keys():  # type: ignore
            for meal, grill in grill_dict[day].items():
                if meal == "BRUNCH":
                    meal = "LUNCH"
                
                meal = meal[0] + meal[1:].lower()
                
                self.menu[day][meal]["Grill"] = grill
        
    def _get_pizza(self):
        pizza_info = self.all_text[5]
        
        def pizza_hier(line: str) -> int:
            if line in ("Pizzas & Pasta", "Available Daily"):
                return -1
            elif line in all_days:
                return 1
            elif line.lower() in ("lunch", "brunch", "dinner"):
                return 2
            elif "Bar" in line:
                return -1
            else:
                return 3

        pizza_tree = Tree.from_list(pizza_info, pizza_hier)
        pizza_dict = pizza_tree.to_dict()["root"]  # type: ignore

        for day in pizza_dict.keys():  # type: ignore
            for meal, pizza in pizza_dict[day].items():
                if meal == "BRUNCH":
                    meal = "LUNCH"
                
                meal = meal[0] + meal[1:].lower()
                
                self.menu[day][meal]["Pizza"] = pizza
            

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
                self.section_dict[dotw[dotw_index - 1]] += (
                    self._clean_str(node.text)
                )
            node = node.find_next()

        for day in dotw:
            self.section_dict[day] = self.section_dict[day].strip()

        return self.section_dict


if __name__ == "__main__":
    d = DiningInfoManager()
    # lunch_specials = d.get_lunch_specials()
    # print(lunch_specials)
    # with open("lunch_specials.txt", "w") as outfile:
    # 	json.dump(lunch_specials, outfile, indent=4)

    # entrees = d.get_entrees()
    # print(entrees)
    # with open("entrees.txt", "w") as outfile:
    # 	json.dump(entrees, outfile, indent=4)
    d.parse_menu()
