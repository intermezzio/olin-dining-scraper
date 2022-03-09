import schedule
import time
import datetime
from message import MessageGenerator
from send import send_mail

m = MessageGenerator()

def get_meal(day, meal):
	print(f"Getting {day} {meal}")
	global m
	msg = m.generate_message(day, meal, quotes=3)
	send_mail(recipient="amascillaro@olin.edu",
		subject=f"{day} {meal} at the Dining Hall",
		body=msg
	)

schedule.every().monday.at("07:07").do(lambda: get_meal("Monday", "Breakfast"))
schedule.every().tuesday.at("07:07").do(lambda: get_meal("Tuesday", "Breakfast"))
schedule.every().wednesday.at("07:07").do(lambda: get_meal("Wednesday", "Breakfast"))
schedule.every().thursday.at("07:07").do(lambda: get_meal("Thursday", "Breakfast"))
schedule.every().friday.at("07:07").do(lambda: get_meal("Friday", "Breakfast"))

schedule.every().monday.at("11:11").do(lambda: get_meal("Monday", "Lunch"))
schedule.every().tuesday.at("11:11").do(lambda: get_meal("Tuesday", "Lunch"))
schedule.every().wednesday.at("11:11").do(lambda: get_meal("Wednesday", "Lunch"))
schedule.every().thursday.at("11:11").do(lambda: get_meal("Thursday", "Lunch"))
schedule.every().friday.at("11:11").do(lambda: get_meal("Friday", "Lunch"))

schedule.every().monday.at("16:44").do(lambda: get_meal("Monday", "Dinner"))
schedule.every().tuesday.at("16:44").do(lambda: get_meal("Tuesday", "Dinner"))
schedule.every().wednesday.at("16:44").do(lambda: get_meal("Wednesday", "Dinner"))
schedule.every().thursday.at("16:44").do(lambda: get_meal("Thursday", "Dinner"))
schedule.every().friday.at("16:44").do(lambda: get_meal("Friday", "Dinner"))
schedule.every().saturday.at("16:44").do(lambda: get_meal("Saturday", "Dinner"))
schedule.every().sunday.at("16:44").do(lambda: get_meal("Sunday", "Dinner"))


schedule.every().minute.do(lambda: get_meal("Tuesday", "Dinner"))

while True:
    schedule.run_pending()
    print(f"Dormant {datetime.datetime.now()}")
    time.sleep(20)
