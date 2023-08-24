# send email with content from an API
# implement logging
# make sure that email creds are not in script (external json file)
# PROPERLY handle all exceptions specifically

import requests
import json
import smtplib

URL = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

with open("creds.json", "r") as f:
    creds = json.load(f)
    f.close()

EMAIL = creds["email"]
PASSWORD = creds["password"]
RECIPIENT = EMAIL


def send_email(joke):
    s = smtplib.SMTP("smtp.gmail.com", 587)  # SPECIFIC TO GMAIL
    s.starttls()
    s.login(EMAIL, PASSWORD)
    s.sendmail(EMAIL, RECIPIENT, f"\n{joke}")
    s.quit


def get_joke_content():
    response = requests.get(URL)
    result = response.json()

    if result["error"]:
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
if joke is not None:
    send_email(joke)
