import mysql.connector
from pathlib import Path
from user import TwitterUser

conn = None
cursor = None

# SQL code for initialization
CONNECT_SQL = """
CREATE TABLE IF NOT EXISTS users (
    link VARCHAR(255) PRIMARY KEY,
    bio TEXT,
    following INT,
    followers INT,
    location VARCHAR(255),
    website VARCHAR(255)
);
"""

# SQL code for storing user
STORE_SQL = """
INSERT INTO users (link, bio, following, followers, location, website)
VALUES (%s, %s, %s, %s, %s, %s);
"""


def connect(user, host, password):
    global conn, cursor

    conn = mysql.connector.connect(
        user=user,
        host=host,
        password=password,
        database="twitterbase",
        interactivity_timeout=1000,
    )

    cursor = conn.cursor()
    cursor.execute(CONNECT_SQL)

    conn.commit()


# if user exists, why bother scraping again?
def user_exists(link) -> bool:
    global cursor

    query = "SELECT COUNT(*) FROM twitter_users WHERE link = %s"
    cursor.execute(query, (link,))
    result = cursor.fetchone()
    return result[0] > 0


def store(user: TwitterUser):
    global cursor, conn

    data = (
        user.link,
        user.bio,
        user.following,
        user.followers,
        user.location,
        user.website,
    )

    cursor.execute(STORE_SQL, data)

    conn.commit()


def close():
    global cursor, conn

    cursor.close()
    conn.close()
