# https://www.bacancytechnology.com/blog/flask-jwt-authentication

from flask import current_app, Blueprint, jsonify, make_response, request
from functools import wraps
import uuid
import jwt
import datetime
import time
import psycopg2
import psycopg2.extras
from config import Config
from app import db
from app.models import User, Friend
from sqlalchemy import func

# host = os.environ.get("DATABASE_HOST")
# user = os.environ.get("DATABASE_USER")
# password = os.environ.get("DATABASE_PASSWORD")
# port = os.environ.get("DATABASE_PORT")
# dbname = os.environ.get("DATABASE_NAME")

# connection = psycopg2.connect(url)
# connection = psycopg2.connect(host=Config.HOST, database=Config.DBNAME, user=Config.USER, password=Config.PASSWORD, port=Config.PORT)

# Allows for use of @token_required. Token is passed in the HTTP header, decoded, and made available to relevant route functions.
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # print(request.headers)
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return make_response('a valid token is missing',  400)
        
        try:
            # TODO: WHEN TOKEN EXPIRES, USER SHOULD BE ASKED TO LOGIN AGAIN
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            # TODO: CHANGE THIS QUERY TO POSTGRES
            # current_user = Users.query.filter_by(public_id=data['public_id']).first()

            current_user = User.query.filter_by(id=data["id"]).first().id


            # with connection:
            #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            #         cursor.execute('SELECT id FROM public."user" WHERE id=%s', (data["id"],))

            #         row = cursor.fetchone()["id"]

            #         current_user = row

        except:
            return make_response('token is invalid',  400)

        return f(current_user, *args, **kwargs)
    return decorator
