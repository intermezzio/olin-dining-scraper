import os
import sys
import traceback
import time
import datetime
import schedule
from message_html import MessageGenerator
from send import send_mail, email_recipients, debug_email, email_bot
from dining import DiningInfoManager

prefix = ""

postfix = "Quotes stated above are, in fact, slanderous, and no, I <b>did not</b> ask anyone for permission before attributing these comments to them."

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


def get_day_no_email(day):
    print(f"Getting {day}")
    d = DiningInfoManager()
    d.parse_menu()
    msg = MessageGenerator.from_dh(d, day)
    msg.export()


def get_day(day):
    global prefix
    try:
        print(f"Getting {day}")
        d = DiningInfoManager()
        d.parse_menu()
        msg = MessageGenerator.from_dh(d, day)
        msg.export()

        # msg = caption + "\n\n" + prefix + ("\n\n" if prefix else "") + msg + ("\n" if postfix else "") + postfix

        print(f"{len(email_recipients)} email addresses")
        print(email_recipients)

        for recipient in email_recipients:
            send_mail(
                recipient=recipient,
                subject=f"{day} at the Dining Hall",
                body=str(msg),
            )
    except Exception:
        error_info = traceback.format_exc()
        print("Exception")
        print(error_info)
        send_mail(
            recipient=debug_email,
            subject=f"[error] {day} at the Dining Hall",
            body=error_info,
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
    if datetime.datetime.today() < datetime.datetime.fromisoformat("2023-03-19"):
        print("Spring break! No menu")
    elif len(sys.argv) >= 2 and sys.argv[1] == "debug":
        print("Debug now")
    elif len(sys.argv) >= 2 and sys.argv[1] == "once":
        print("once")
        dotw = datetime.datetime.today().strftime("%A")
        get_day(dotw)
    elif len(sys.argv) >= 2 and sys.argv[1] == "local":
        print("local")
        dotw = datetime.datetime.today().strftime("%A")
        get_day_no_email(dotw)
    else:
        print("Set up scheduling")
        while True:
            schedule.run_pending()
            print(f"Real Dormant {datetime.datetime.now()}")
            time.sleep(30)
