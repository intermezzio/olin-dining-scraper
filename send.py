import yagmail
import json
import os

class UrInsecureException(Exception):
	pass

try:
	with open("assets/config.json") as infile:
		config = json.load(infile)
		email = config["email"]
		password = os.environ.get('PASSWORD', config["password"])
	yag = yagmail.SMTP(email, password)
except Exception:
	raise UrInsecureException(f"You don't have the proper credentials for this, user: {email} pass: {password}")

def send_mail(recipient="amascillaro@olin.edu", subject = "Meal Update", body="test", attachment=[]):
	global yag
	yag.send(
	    to=recipient,
	    subject=subject,
	    contents=body, 
	    attachments=attachment
	)

