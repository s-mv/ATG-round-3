import csv
import scraper

links: [str] = []

with open("twitter_links.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        links.append(row[0])

information = []

for link in links:
    info = scraper.scrape_twitter_link(link)
    if info != None:
        information.append(info)

print(information)
