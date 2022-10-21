# Driving-Behaviours-Web-Server
Python Flask web server for a REST API endpoint to interact with database backend

[![Python application](https://github.com/ReeceNich/Driving-Behaviours-Web-Server/actions/workflows/pytest.yml/badge.svg)](https://github.com/ReeceNich/Driving-Behaviours-Web-Server/actions/workflows/pytest.yml)

# Preparing the Virtual Environment:
python -m venv .venv
source .venv/bin/activate   # different in windows
pip install flask

## Start flask server in development mode
Create a `.flaskenv` file in the root directory and add the following text:
FLASK_APP=app
FLASK_DEBUG=1

pip install python-dotenv

You can now run the flask server in development mode using `flask run` in the command line.

## Adding HTTPS for development server
Note: Browsers will not like the certificate as it is self-signed.
pip install pyopenssl

Add `FLASK_RUN_CERT='adhoc'` to the `.flaskenv` file.

## Install PostgreSQL library for Python
pip install psycopg2-binary

Create a `.env` file and add:
DATABASE_HOST=host
DATABASE_USER=username
DATABASE_PASSWORD=password
DATABASE_PORT=5432
DATABASE_NAME=dbname
FLASK_SECRET_KEY=secretkey

Generate secret key by using:
import secrets
secrets.token_hex(16)


## Start flask server in production mode
pip3 install gunicorn
gunicorn -w 2 -b 0.0.0.0:80 'app:app'