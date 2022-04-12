import yagmail
import json
import os

class UrInsecureException(Exception):
	pass

try:
	with open("assets/config.json") as infile:
		config = json.load(infile)
		
		email_addr_str = os.environ.get("EMAIL_ADDRS", config["email"])

		# all email recipients
		email_addrs = list(filter(lambda x: x, email_addr_str.split(",")))
		# personal email for project maintainer
		debug_email = email_addrs[1]
		# email recipients (excluding the bot)
		email_recipients = email_addrs[1:]
		
		# bot credentials
		email_bot = email_addrs[0]
		password = os.environ.get('PASSWORD', config["password"])
	yag = yagmail.SMTP(email_bot, password)
except Exception:
	raise UrInsecureException(f"You don't have the proper credentials for this")

def send_mail(recipient=debug_email, bcc=None, subject = "Meal Update", body="test", attachment=[],
		contents=[]):
	global yag
	try:
		yag.send(
		    to=recipient,
		    bcc=bcc,
		    subject=subject,
		    contents=contents+[body], 
		    attachments=attachment,
		)
	except Exception as e:
		print(e)
		raise UrInsecureException(f"You don't have the proper credentials for this")

