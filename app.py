import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask
import time

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
host = os.environ.get("DATABASE_HOST")  # gets variables from environment
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")
port = os.environ.get("DATABASE_PORT")
dbname = os.environ.get("DATABASE_NAME")


# connection = psycopg2.connect(url)
connection = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)



@app.get("/api/livespeed")
def get_live_speed():
    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM public."LiveSpeed"')

            allRows = cursor.fetchall()

            print(allRows)
    
    return {
        "dateFetched": int(time.time()),
        "data": allRows
    }