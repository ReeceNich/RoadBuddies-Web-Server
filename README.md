# Driving-Behaviours-Web-Server
Python Flask web server for a REST API endpoint to interact with database backend

[![Python application](https://github.com/ReeceNich/Driving-Behaviours-Web-Server/actions/workflows/pytest.yml/badge.svg)](https://github.com/ReeceNich/Driving-Behaviours-Web-Server/actions/workflows/pytest.yml)

# Preparing the Virtual Environment:
```
python -m venv .venv
source .venv/bin/activate   # different in windows
pip install -r requirements.txt
```

## Configure flask server (in development mode)
Create a `.flaskenv` file in the root directory and add the following text:
```
FLASK_APP=app
FLASK_DEBUG=1
```

## Configuring SQLAlchemy for PostgreSQL in Python

Create a `.env` file and add:
```
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<dbname>
FLASK_SECRET_KEY=secretkey
```

Generate secret key in Python by using:
```
import secrets
secrets.token_hex(16)
```

## Server is now configured
You can now run the flask server in development mode using `flask run` in the command line.


## Adding HTTPS for development server (optional)
Note: Browsers will not like the certificate as it is self-signed.
```
pip install pyopenssl
```

Add `FLASK_RUN_CERT='adhoc'` to the `.flaskenv` file.




# Start flask server in production mode
Running the server in production mode is important for security and will remove the debugger which is used in the development server.
```
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:80 '<file/module name>:<flask app variable>'
gunicorn -w 2 -b 0.0.0.0:80 'run:app'
gunicorn -w 2 -b 0.0.0.0:80 --config gunicorn.conf.py 'run:app'
```

# Testing
To run the tests, make sure the environment is active.
Enter the command into the terminal:
```
pytest
```

## Configuring the test for specific environments
The tests can either be run in a temporary testing environment or in the production test environment.

In `tests/conftest.py`, you can set the parameter in the `create_app(<config>)` function to the following options:
- `TestConfig` - this uses a temporary database in SQLite stored in memory.
- `TestProdConfig` - this uses a PostgreSQL database for testing. Create a separate database to your production database to ensure existing data is not altered.

The Config classes and values are found in `config.py` in the root directory.

https://flask.palletsprojects.com/en/2.2.x/testing/