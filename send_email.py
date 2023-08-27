# send email with content from an API
# implement logging
# make sure that email creds are not in script (external json file)
# PROPERLY handle all exceptions specifically

import requests
import json
import smtplib
import logging

URL = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

with open("creds.json", "r") as f:
    creds = json.load(f)
    f.close()

LOGFILE = "send-email.log"
EMAIL = creds["email"]
PASSWORD = creds["password"]
RECIPIENT = EMAIL

logging.basicConfig(
    filemode="a",
    filename=LOGFILE,
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)


def send_email(joke):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)  # SPECIFIC TO GMAIL
        s.starttls()
    except smtplib.SMTPConnectError:
        logging.error("Could not connect to the mail server")
        exit()
    try:
        s.login(EMAIL, PASSWORD)
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication Failure")
        exit()

    try:
        s.sendmail(EMAIL, RECIPIENT, f"\n{joke}")
    except smtplib.SMTPException:
        logging.error("Unable to send email due to error")
        exit()
    s.quit


def get_joke_content():
    response = requests.get(URL)
    result = response.json()
    if result["error"]:
        logging.error("Something went wrong with the request to the API.")
        return None
    if result["type"] == "twopart":
        # extract a setup and delivery
        setup = result["setup"]
        delivery = result["delivery"]
        return f"Setup: {setup}\nDelivery: {delivery}"

    else:
        # extract a joke
        joke = result["joke"]
        return f"Joke: {joke}"


joke = get_joke_content()
logging.info("Joke retrieved successfully")
if joke is not None:
    send_email(joke)
    logging.info("Email successfully sent")
