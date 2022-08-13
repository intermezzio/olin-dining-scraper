import random
import random_stuff as rs
import re

class Quotes:
	def __init__(self):
		self.substitution_data = (
			(r"{address}", rs.get_address),
			(r"{appliance}", rs.get_appliance),
			(r"{beer_brand}", rs.get_beer_brand),
			(r"{capital}", rs.get_capital),
			(r"{car}", rs.get_car),
			(r"{country}", rs.get_country),
			(r"{credit_card}", rs.get_credit_card),
			(r"{food}", rs.get_food),
			(r"{hipster}", rs.get_hipster),
			(r"{ingredient}", rs.get_ingredient),
			(r"{ip_addr}", rs.get_ip_addr),
			(r"{language}", rs.get_language),
			(r"{full_name}", rs.get_name),
			(r"{nationality}", rs.get_nationality),
			(r"{num}", rs.get_number),
			(r"{phone_number}", rs.get_phone_number),
			(r"{ssn}", rs.get_ssn),
		)
		self.tag_remover = re.compile(r'<[^>]+>')
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

		with open("assets/marketing.txt") as infile:
			self.marketing = infile.read().strip().split("\n")

	def get_adjective(self, n=1, quote_only=True):
		return self._from_templates([r"{adj}"]*n, n=n, quote_only=quote_only)

	def get_class(self, n=1, quote_only=True):
		return self._from_templates([r"{class}"]*n, n=n, quote_only=quote_only)

	def get_eat(self, n=1, quote_only=True):
		return self._from_templates([r"{eat}"]*n, n=n, quote_only=quote_only)

	def get_name(self, n=1, quote_only=True):
		return self._from_templates([r"{name}"]*n, n=n, quote_only=quote_only)
		

	def get_marketing(self, n=1):
		bases = self._choose_n(self.marketing, n)
		return self._from_templates(bases, n=n, quote_only=True)

	def get_quotes(self, item_list, n=1, quote_only=False, html_tags=True):
		bases = self._choose_n(self.comments, n)
		return self._from_templates(bases, n=n, item_list=item_list, quote_only=quote_only,
			html_tags=html_tags)

	def _from_templates(self, bases, item_list=None, n=1, quote_only=False,
			html_tags=True):
		adjs = self._choose_n(self.adjectives, n)
		classes = self._choose_n(self.classes, n)
		eats = self._choose_n(self.eat, n)
		names = self._choose_n(self.names, n)
		items = self._choose_n(item_list, n) if item_list else [""] * n

		quotes = list()
		for b, a, c, e, n, i in zip(bases, adjs, classes, eats, names, items):
			if not quote_only:
				b = "\"" + b + "\"\n\t- " + r"{name}" # add double quotes and name
			b = b.replace(r"{item}", i)
			b = b.replace(r"{adj}", a)
			b = b.replace(r"{eat}", e)
			b = b.replace(r"{class}", c)
			b = b.replace(r"{name}", n)
			b = self.substitute_random_api(b)
			if not html_tags:
				b = self.tag_remover.sub('', b)
			quotes.append(b)

		return quotes

	def substitute_random_api(self, base):
		for substr, func in self.substitution_data:
			base = base.replace(substr, func()[0]) if substr in base else base

		return base

	def _shuffle_all(self):
		random.shuffle(self.adjectives)
		random.shuffle(self.classes)
		random.shuffle(self.comments)
		random.shuffle(self.eat)
		random.shuffle(self.names)
		random.shuffle(self.marketing)

	def _choose_n(self, asset, n=1):
		if n < len(asset):
			return random.sample(asset, n)
		else:
			return random.choices(asset, k=n)