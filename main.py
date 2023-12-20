import csv
from datetime import datetime
import scraper

links = []

with open("twitter_links.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        links.append(row[0])

users = scraper.scrape_twitter(links)

# convert the data to CSV
output_path = f"./out/data-{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.csv"

# finally save the data
with open(output_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Link", "Bio", "Following", "Followers", "Location", "Website"])

    for user in users:
        writer.writerow(
            [
                user.link,
                user.bio,
                user.following,
                user.followers,
                user.location,
                user.website,
            ]
        )

print(f"CSV saved at: {output_path}")