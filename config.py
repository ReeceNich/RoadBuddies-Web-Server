from mimetypes import init
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file into environment


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    HOST = os.environ.get("DATABASE_HOST")
    USER = os.environ.get("DATABASE_USER")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")
    PORT = os.environ.get("DATABASE_PORT")
    DBNAME = os.environ.get("DATABASE_NAME")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    print(os.environ.get("DATABASE_HOST"))