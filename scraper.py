from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from collections import deque
import logging
from threading import Thread
import re

selectors = {
    "Container": "[data-testid='primaryColumn']",
    "Bio": "[data-testid='UserDescription']",
    "FollowingFollowers": ".css-175oi2r:not(.r-1mf7evn) .r-bcqeeo.r-qvutc0.r-poiln3.r-1b43r93.r-1cwl3u0.r-b88u0q span",
    "Location": "[data-testid='UserLocation']",
    "Website": "[data-testid='UserUrl']",
}

driver: webdriver.Firefox


class TwitterUser:
    link: str  # for reference
    bio: str
    following: int
    followers: int
    location: str
    website: str

    def __init__(self, link, bio, following, followers, location, website):
        self.link = link
        self.bio = bio
        self.following = following
        self.followers = followers
        self.location = location
        self.website = website


""" 
Flow of operations:
1. Initialise the webdriver             with `start_scraping_twitter`.
2. Scrape raw data from the given links with `scrape_raw_twitter_data`
4. Free driver
3. Get needed information from data     with `structure_twitter_data`  (threaded)
5. Stop
"""


def scrape_twitter(links: [str], log: bool = True) -> [TwitterUser]:
    information = deque()
    data: [TwitterUser] = []

    saved_logging_level = logging.getLogger().getEffectiveLevel()

    if log:
        logging.getLogger().setLevel(logging.INFO)

    # 1. Initialise the webdriver
    logging.info("Initialising driver.")
    start_scraping_twitter()
    # 2. Scrape raw data from the given links
    logging.info("Scraping data. This may take long.")
    scrape_raw_twitter_data(links, information)
    logging.info("Scraping done. Quitting driver.")
    # 3. Free driver
    driver.quit()
    logging.info("Extracting useful information.")
    # 4. Scrape needed information from data (threaded)
    for _ in range(4):
        Thread(target=structure_twitter_data, args=(information, links, data)).start()

    # only continute once the threads are done
    while len(information) != 0:
        pass

    logging.info("All done.")

    logging.getLogger().setLevel(saved_logging_level)

    return data


def start_scraping_twitter():
    global driver

    # firefox is probably the best familiar enough option out there
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)


def scrape_raw_twitter_data(links: [str], information: deque):
    global driver

    for link in links:
        driver.get(link)
        # essential exception handling since we don't want to stop at any point
        try:
            # waiting for "FollowingFollowers" instead of "Container"
            # this is because it's the last useful set of elements in the container
            # Twitter isn't very kind to users that aren't logged in
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, selectors["FollowingFollowers"])
                )
            )
        except:
            logging.exception(f"Exception with link {link}")
            links.remove(link)  # completely get rid of the link
            continue

        container = driver.find_element(
            By.CSS_SELECTOR, selectors["Container"]
        ).get_attribute("innerHTML")
        information.append(container)


def structure_twitter_data(information: deque, links, data: [TwitterUser]):
    # this is why deques are superior to generic queues!
    # they're also thread-safe (and this function is going to run on threads)
    while len(information) != 0:
        i = information.popleft()
        link = links.pop(0)

        # bs4 handles from this point since we don't need resource heavy selenium anymore
        soup = BeautifulSoup(i, "html.parser")
        bio = soup.select_one(selectors["Bio"])

        # since following and follower count both have the same CSS selector,
        # we'll get an array with 2 elements in it
        following_followers = soup.select(selectors["FollowingFollowers"])
        # substitution of K, M, L (lakh), etc. is required here
        for i in range(len(following_followers)):
            value = following_followers[i].text.upper()  # for case insensitivity
            # using regex to match the value and suffix
            matching = re.compile(r"(\d+(\.\d+)?)\s*([KLM]?)").match(value)

            if matching:
                number, _, suffix = matching.groups()
                multiplier = {
                    "K": 10**3,  # thousand
                    "L": 10**5,  # lakh
                    "M": 10**6,  # million
                }.get(suffix, 1)

                following_followers[i] = int(float(number) * multiplier)
            # if it doesn't match, we'll still extract the information as a string

        following = following_followers[0]
        followers = following_followers[1]

        location = soup.select_one(selectors["Location"])
        website = soup.select_one(selectors["Website"])

        user = TwitterUser(
            link,
            bio.text if bio else None,
            following,
            followers,
            location.text if location else None,
            website.text if website else None,
        )

        data.append(user)
