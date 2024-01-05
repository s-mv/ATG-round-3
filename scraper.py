from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import logging
from multiprocessing import Process, Manager, Queue, Lock
import re

from db import user_exists
from user import TwitterUser

selectors = {
    "Container": "[data-testid='primaryColumn']",
    "Bio": "[data-testid='UserDescription']",
    "FollowingFollowers": ".css-175oi2r:not(.r-1mf7evn) .r-bcqeeo.r-qvutc0.r-poiln3.r-1b43r93.r-1cwl3u0.r-b88u0q span",
    "Location": "[data-testid='UserLocation']",
    "Website": "[data-testid='UserUrl']",
}

""" 
Flow of operations:
1. Initialise the webdriver  
2. Scrape raw data from the given links with `scrape_raw_twitter_data` (threaded)
4. Free driver
3. Get needed information from data     with `structure_twitter_data`
5. Stop
"""


def scrape_twitter(links: [str], log: bool = True, num_procs: int = 2) -> [TwitterUser]:
    manager = Manager()
    information_queues = [manager.Queue() for _ in range(num_procs)]
    data_queue = manager.Queue()
    links_q = manager.Queue()

    # populate the links queue
    for link in links:
        links_q.put(link)
    # add in None for processes to terminate
    for _ in range(num_procs):
        links_q.put(None)

    saved_logging_level = logging.getLogger().getEffectiveLevel()

    if log:
        logging.getLogger().setLevel(logging.INFO)

    # Steps 1., 2., 3. on threads
    logging.info("Scraping data. This may take long.")

    processes = []
    locks = [manager.Lock() for _ in range(num_procs)]

    # this is necessary for multithreading to be smooth
    for i in range(num_procs):
        proc = Process(
            target=scrape_raw_twitter_data,
            args=(links_q, information_queues[i], locks[i]),
        )
        proc.start()
        processes.append(proc)
    for proc in processes:
        proc.join()
        print(f"Process {proc.pid} finished.")

    logging.info("Scraping done. Quitting driver.")

    # Step 4. on threads
    logging.info("Extracting useful information.")
    processes = []

    # adding None for multiprocessing
    for _ in range(num_procs):
        for q in information_queues:
            q.put(None)

    for i in range(num_procs):
        proc = Process(
            target=structure_twitter_data,
            args=(information_queues[i], data_queue, locks[i]),
        )
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()

    # finally step 5. (all done)
    logging.info("All done.")

    logging.getLogger().setLevel(saved_logging_level)

    return_data = []
    while not data_queue.empty():
        return_data.append(data_queue.get())

    print(links_q.qsize(), data_queue.qsize())

    return return_data


def scrape_raw_twitter_data(links: Queue, information: Queue, lock: Lock):
    # Step 1.
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    container = None

    # Step 2.
    while True:
        with lock:
            link = links.get()
        if link is None:
            break  # exit condition

        with lock:
            if user_exists(link):
                continue

        logging.info(f"processing {link}")
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
            container = driver.find_element(
                By.CSS_SELECTOR, selectors["Container"]
            ).get_attribute("innerHTML")
            num_remaining = links.qsize()
        except:
            # if it's a bad link
            logging.warning(f"{link} failed.")
            continue

        information.put(
            {
                "html": container,
                "link": link,
            }
        )
        logging.info(f"{link} successfully scraped.")

    # Step 3.
    driver.quit()


def structure_twitter_data(information: Queue, data: [TwitterUser], lock: Lock):
    while True:
        with lock:
            info = information.get()
        if info is None:
            break  # this is the exit condition

        # bs4 handles from this point since we don't need resource heavy selenium anymore
        soup = BeautifulSoup(info["html"], "html.parser")
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
            info["link"],
            bio.text if bio else None,
            following,
            followers,
            location.text if location else None,
            website.text if website else None,
        )

        data.put(user)
