import schedule
import time
import datetime
from message import MessageGenerator
from send import send_mail
import os

m = MessageGenerator()

def get_meal(day, meal):
	try:
		print(f"Getting {day} {meal}")
		global m
		msg = m.generate_message(day, meal, quotes=3)
		email_addr_str = os.environ.get("EMAIL_ADDRS", '')
		email_addrs = list(filter(lambda x: x, email_addr_str.split(",")))
		print(f"{len(email_addrs)} email addresses")
		for addr in email_addrs:
			send_mail(recipient=addr,
				subject=f"{day} {meal} at the Dining Hall",
				body=msg
			)
	except Exception as e:
		print("Exception")
		print(e)
		send_mail(recipient="amascillaro@olin.edu",
			subject=f"Olin Dining Scraper Error",
			body=e
		)

schedule.every().monday.at("11:07").do(lambda: get_meal("Monday", "Breakfast"))
schedule.every().tuesday.at("11:07").do(lambda: get_meal("Tuesday", "Breakfast"))
schedule.every().wednesday.at("11:07").do(lambda: get_meal("Wednesday", "Breakfast"))
schedule.every().thursday.at("11:07").do(lambda: get_meal("Thursday", "Breakfast"))
schedule.every().friday.at("11:07").do(lambda: get_meal("Friday", "Breakfast"))

schedule.every().monday.at("15:11").do(lambda: get_meal("Monday", "Lunch"))
schedule.every().tuesday.at("15:11").do(lambda: get_meal("Tuesday", "Lunch"))
schedule.every().wednesday.at("15:11").do(lambda: get_meal("Wednesday", "Lunch"))
schedule.every().thursday.at("15:11").do(lambda: get_meal("Thursday", "Lunch"))
schedule.every().friday.at("15:11").do(lambda: get_meal("Friday", "Lunch"))

schedule.every().monday.at("20:44").do(lambda: get_meal("Monday", "Dinner"))
schedule.every().tuesday.at("20:44").do(lambda: get_meal("Tuesday", "Dinner"))
schedule.every().wednesday.at("20:44").do(lambda: get_meal("Wednesday", "Dinner"))
schedule.every().thursday.at("20:44").do(lambda: get_meal("Thursday", "Dinner"))
schedule.every().friday.at("20:44").do(lambda: get_meal("Friday", "Dinner"))
schedule.every().saturday.at("20:44").do(lambda: get_meal("Saturday", "Dinner"))
schedule.every().sunday.at("20:44").do(lambda: get_meal("Sunday", "Dinner"))

# while True:
#     schedule.run_pending()
#     print(f"Dormant {datetime.datetime.now()}")
#     time.sleep(30)
