import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

conn = mysql.connector.connect(
    user=config.get("DatabaseCredentials", "user"),
    host=config.get("DatabaseCredentials", "host"),
    password=config.get("DatabaseCredentials", "password"),
    database="twitterbase",
)

cursor = conn.cursor()

select_query = "SELECT * FROM users"
cursor.execute(select_query)

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
