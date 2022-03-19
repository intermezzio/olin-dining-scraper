# Olin Dining Scraper

This scraper reads Olin College of Engineering's Dining Hall menu from their website and sends emails regarding the daily menu items. It is built with Python, using BeatutifulSoup to download the website content and yagmail to send emails. The code is hosted on a Heroku App.

To host your own version of this, click the deploy button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/intermezzio/olin-dining-scraper)

## Setup

For security purposes, the online version of this repository does not have passwords and recipients' email addresses stored in it. Currently, there are two ways to set up these credentials for deployment.

### Option 1: Environment Variables (preferred)

This option is great for hosting on another cloud platform because you can set environment variables within, say, Heroku itself and the information is never placed in the GitHub repository. In this case, you will want to define two variables:

`EMAIL_ADDRS`: a comma separated list of emails for the bot, debug email, and recipients.

The bot is a gmail address set up to send mail from these Python scripts (it must be gmail to use the yagmail package). To set this bot up, sign in to your account and navigate [here](https://www.google.com/settings/security/lesssecureapps) to enable Python to send emails from the address.

The debug email should be the maintainer's personal email address. This is where all emails about errors in the code are sent.

The other recipients include anyone else who wants to receive emails about the dining hall food.

`PASSWORD`: a string containing the password to the bot email.

**Example config:**

```sh
export EMAIL_ADDRS="mybot@gmail.com,mypersonalemail@olin.edu,fanaticdininghalleater@olin.edu,otherrecipient@olin.edu"
export PASSWORD="mysupersecurepassword"
```

### Option 2: config.json

Alternatively, if you don't want to use environment variables, place the email address list and password in the `assets/config.json` file under the attributes "email" and "password". This is faster to set up but should not be pushed to GitHub or shared publicly.

## Contributing

Features, comment ideas, and all possible improvements are encouraged. The comments this script generates about menu items are randomly chosen from the `assets/*.txt` files, where random comment templates, adjectives, ways to describe eating, and more are auto-generated. Each line in these text files is a possible output. Add any new content to the bottom of these files and make a pull request to have your comments possibly featured in a future email! All other changes can be requested with an issue or a pull request.