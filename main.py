import configparser
import csv
from datetime import datetime
import db
import scraper

links = []

with open("twitter_links.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        links.append(row[0])

config = configparser.ConfigParser()
config.read("config.ini")

db.connect(
    user=config.get("DatabaseCredentials", "user"),
    host=config.get("DatabaseCredentials", "host"),
    password=config.get("DatabaseCredentials", "password"),
)

users = scraper.scrape_twitter(links)

for user in users:
    db.store(user)

db.close()
