from mysql.connector import pooling
from user import TwitterUser

pool = None # pool of connections

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


def connect(user, host, password, size=32):
    global pool

    # creates a connection pool (for multiprocessing)
    pool = pooling.MySQLConnectionPool(
        user=user,
        host=host,
        pool_name="twitterbase_pool",
        pool_size=size,
        password=password,
        database="twitterbase",
    )

    conn = pool.get_connection()

    cursor = conn.cursor()
    cursor.execute(CONNECT_SQL)

    conn.commit()


# if user exists, why bother scraping again?
def user_exists(link) -> bool:
    global pool

    conn = pool.get_connection()
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM users WHERE link = %s"
    cursor.execute(query, (link,))
    result = cursor.fetchone()
    return result[0] > 0


def store(user: TwitterUser):
    global pool

    conn = pool.get_connection()
    cursor = conn.cursor()

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
