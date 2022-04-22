import os
import sys
import traceback
import time
import datetime
import schedule
import yagmail
from message import MessageGenerator
from send import send_mail, email_recipients, debug_email, email_bot

prefix = ""

postfix = """\"Some people would pay $25 to eat RiceBurg while living at Olin, but I tell you, I'd pay 7*$25 to eat oak cask aged New England Fish Friday in the dining hall instead!\"
\t- Jaclyn\n"""

# def get_meal(day, meal):
# 	global prefix
# 	try:
# 		print(f"Getting {day} {meal}")
# 		m = MessageGenerator()
# 		msg = m.generate_message(day, meal, quotes=2)
		
# 		msg = prefix + ("\n\n" if prefix else "") + msg + ("\n\n" if postfix else "") + postfix

# 		print(f"{len(email_recipients)} email addresses")
# 		print(email_recipients)

# 		for recipient in email_recipients:
# 			send_mail(recipient=recipient,
# 				subject=f"{day} {meal} at the Dining Hall",
# 				body=msg,
# 				attachment="menu.json"
# 			)
# 	except Exception as e:
# 		print("Exception")
# 		print(e)
# 		send_mail(recipient=debug_email,
# 			subject=f"Olin Dining Scraper Error",
# 			body=e
# 		)

def get_day(day):
	global prefix
	try:
		print(f"Getting {day}")
		m = MessageGenerator()
		msg, caption = m.generate_day_message(day, quotes=2)
		
		msg = caption + "\n\n" + prefix + ("\n\n" if prefix else "") + msg + ("\n" if postfix else "") + postfix
		
		print(f"{len(email_recipients)} email addresses")
		print(email_recipients)
		
		for recipient in email_recipients:
			send_mail(recipient=recipient,
				subject=f"{day} at the Dining Hall",
				body=msg,
				attachment="menu.json",
				contents=[yagmail.inline("featured_img.png")]
			)
	except Exception:
		error_info = traceback.format_exc()
		print("Exception")
		send_mail(recipient=debug_email,
			subject=f"[error] {day} at the Dining Hall",
			body=error_info
		)

# EDT = UTC-4, these times are 4 hours ahead
schedule.every().monday.at("10:42").do(lambda: get_day("Monday"))
schedule.every().tuesday.at("10:42").do(lambda: get_day("Tuesday"))
schedule.every().wednesday.at("10:42").do(lambda: get_day("Wednesday"))
schedule.every().thursday.at("10:42").do(lambda: get_day("Thursday"))
schedule.every().friday.at("10:42").do(lambda: get_day("Friday"))

schedule.every().saturday.at("10:42").do(lambda: get_day("Saturday"))
schedule.every().sunday.at("10:42").do(lambda: get_day("Sunday"))

# schedule.every().monday.at("11:07").do(lambda: get_meal("Monday", "Breakfast"))
# schedule.every().tuesday.at("11:07").do(lambda: get_meal("Tuesday", "Breakfast"))
# schedule.every().wednesday.at("11:07").do(lambda: get_meal("Wednesday", "Breakfast"))
# schedule.every().thursday.at("11:07").do(lambda: get_meal("Thursday", "Breakfast"))
# schedule.every().friday.at("11:07").do(lambda: get_meal("Friday", "Breakfast"))

# schedule.every().monday.at("15:11").do(lambda: get_meal("Monday", "Lunch"))
# schedule.every().tuesday.at("15:11").do(lambda: get_meal("Tuesday", "Lunch"))
# schedule.every().wednesday.at("15:11").do(lambda: get_meal("Wednesday", "Lunch"))
# schedule.every().thursday.at("15:11").do(lambda: get_meal("Thursday", "Lunch"))
# schedule.every().friday.at("15:11").do(lambda: get_meal("Friday", "Lunch"))

# schedule.every().monday.at("20:44").do(lambda: get_meal("Monday", "Dinner"))
# schedule.every().tuesday.at("20:44").do(lambda: get_meal("Tuesday", "Dinner"))
# schedule.every().wednesday.at("20:44").do(lambda: get_meal("Wednesday", "Dinner"))
# schedule.every().thursday.at("20:44").do(lambda: get_meal("Thursday", "Dinner"))
# schedule.every().friday.at("20:44").do(lambda: get_meal("Friday", "Dinner"))
# schedule.every().saturday.at("20:44").do(lambda: get_meal("Saturday", "Dinner"))
# schedule.every().sunday.at("20:44").do(lambda: get_meal("Sunday", "Dinner"))

if __name__ == "__main__":
	if len(sys.argv) >= 2 and sys.argv[1] == "debug":
		print("Debug now")
	else:
		print("Set up scheduling")
		while True:
			 schedule.run_pending()
			 print(f"Dormant {datetime.datetime.now()}")
			 time.sleep(30)
