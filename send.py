import yagmail
import json

class UrInsecureException(Exception):
	pass

try:
	with open("assets/config.json") as infile:
		config = json.load(infile)
		email = config["email"]
		password = config["password"]
	yag = yagmail.SMTP(email, password)
except Exception:
	raise UrInsecureException("You don't have the proper credentials for this")

def send_mail(recipient="amascillaro@olin.edu", subject = "Meal Update", body="test", attachment=[]):
	global yag
	yag.send(
	    to=recipient,
	    subject=subject,
	    contents=body, 
	    attachments=attachment
	)

