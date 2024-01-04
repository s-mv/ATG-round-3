import csv
from datetime import datetime
import scraper
import db

links = []

with open("twitter_links.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        links.append(row[0])

users = scraper.scrape_twitter(links)


# convert the data to CSV
db.connect("localhost", "smv", "coffee")
