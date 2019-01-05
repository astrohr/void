#!/usr/bin/python3
"""
Example program to insert image paths into a database.

Usage:
  Setup.py <db> (--user=USER) (--passwd=PASSWORD) (--src=IMAGES_FOLDER_PATH) \
  [--host=HOST] [--port=PORT]

Options:
   -h, --help       Show this message.

"""
import os

import psycopg2
from docopt import docopt

arguments = docopt(__doc__)

# Required args
db = arguments.get("<db>")
user = arguments.get("--user")
passwd = arguments.get("--passwd")
src = arguments.get("--src")

# Optional args
host = arguments.get("--host")
port = arguments.get("--port")

# If optional args are None
if not host:
    host = "127.0.0.1"
if not port:
    port = "5432"

# PostgreSQL opearations
conn = psycopg2.connect(
    database=db, user=user, password=passwd, host=host, port=port)

print("Opened database successfully")

cur = conn.cursor()

# Create table (example only)
cur.execute('''CREATE TABLE OBSERVATIONS
      (ID INT PRIMARY KEY     NOT NULL,
      PATH           TEXT    NOT NULL);''')

print("Table created successfully")

content = os.listdir(src)
imgs = [f for f in content if f.endswith(".fit")]

for i, img in enumerate(imgs):
    cur.execute("INSERT INTO OBSERVATIONS (ID,PATH) \
        VALUES ({}, '{}');".format(i, os.path.abspath(img)))

print("Values inserted succesfully")

conn.commit()
conn.close()
