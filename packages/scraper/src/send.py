# send from yahoo email
import json
import os
from email.message import EmailMessage
from email.mime.text import MIMEText
import smtplib

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

	# create smtp client for sending emails
	smtp_client = smtplib.SMTP('smtp.mail.yahoo.com', 587)
except Exception:
	raise UrInsecureException(f"You don't have the proper credentials for this")


def send_mail(recipient=debug_email, subject = "Meal Update", body="test"):
	global email_bot, password
	
	if isinstance(recipient, str):
		recipient = [recipient]

	email_message = EmailMessage()
	
	email_message["From"] = email_bot
	email_message["To"] = recipient
	email_message["Subject"] = subject
	
	email_message.set_content(body, subtype="html")

	try:
		with smtplib.SMTP('smtp.mail.yahoo.com', 587) as smtp_client:
			smtp_client.ehlo()
			smtp_client.starttls()
			smtp_client.ehlo()
			smtp_client.login(email_bot, password)
			smtp_client.send_message(email_message)
	except Exception as e:
		print(e)
		raise UrInsecureException(f"You don't have the proper credentials for this")