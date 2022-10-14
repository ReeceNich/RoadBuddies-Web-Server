# https://www.bacancytechnology.com/blog/flask-jwt-authentication

from operator import truediv
from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
import time
from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.extras

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)

# gets variables from environment
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")

host = os.environ.get("DATABASE_HOST")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")
port = os.environ.get("DATABASE_PORT")
dbname = os.environ.get("DATABASE_NAME")


# connection = psycopg2.connect(url)
connection = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)




def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # print(request.headers)
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        
        try:
            # TODO: WHEN TOKEN EXPIRES, USER SHOULD BE ASKED TO LOGIN AGAIN
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # TODO: CHANGE THIS QUERY TO POSTGRES
            # current_user = Users.query.filter_by(public_id=data['public_id']).first()

            with connection:
                with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute('SELECT public_id FROM public."Users" WHERE public_id=%s', (data["public_id"],))

                    row = cursor.fetchone()["public_id"]

                    current_user = row

        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/api/register', methods=['POST'])
def signup_user(): 
    data = request.get_json() 
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # TODO: CHANGE THIS QUERY TO POSTGRES
    # new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    # db.session.add(new_user) 
    # db.session.commit()


    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute('INSERT INTO public."Users" (id, public_id, username, password, email, name) VALUES (%s, %s, %s, %s, %s, %s)',
                (str(uuid.uuid4()), str(uuid.uuid4()), data["username"], hashed_password, data["email"], data["name"]))


    return jsonify({'message': 'registered successfully'})


@app.route('/api/login', methods=['POST']) 
def login_user():
    print("login running")
    auth = request.authorization  
    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify auth headers', 401, {'Authentication': 'login required"'})   


    # TODO: CHANGE THIS QUERY TO POSTGRES
    # user = Users.query.filter_by(name=auth.username).first()  

    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            print("AUTHHH: ", auth.username, auth.password)
            cursor.execute('SELECT * FROM public."Users" WHERE LOWER(username)=LOWER(%s)', (auth.username,))

            user = cursor.fetchone()
            print("Login User Row: ", user)


    if check_password_hash(user["password"], auth.password):
        token = jwt.encode({'public_id' : user["public_id"], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=525960)}, app.config['SECRET_KEY'], "HS256")

        return jsonify({'token' : token})

    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@app.route('/api/get/user_info', methods=['GET'])
@token_required
def get_user_info(current_user):
    print("Get user info")
    print(current_user)

    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM public."Users" WHERE public_id=%s', (current_user,))

            user = cursor.fetchone()
            print("Get User Info Row: ", user)
            
    return jsonify(user)


def get_public_id_from_username(username):
    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute('SELECT public_id FROM public."Users" WHERE username=%s', (username,))

            user = cursor.fetchone()
            return user["public_id"]


@app.route("/api/add/latest_location", methods=['POST'])
@token_required
def add_latest_location(current_user):
    data = request.get_json() 

    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""
            INSERT INTO public."LatestLocation" (public_id, latitude, longitude, time)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT(public_id) DO UPDATE
            SET latitude = excluded.latitude,
                longitude = excluded.longitude,
                time = excluded.time
            """,
                (current_user, data["latitude"], data["longitude"], data["time"])
            )
            return jsonify({'message': 'location updated successfully'})


# TODO: Add error handling for existing friend.
@app.route("/api/add/friend", methods=['POST'])
@token_required
def add_friend(current_user):
    data = request.get_json()


    friend_public_id = get_public_id_from_username(data["friend_username"])
    print("Friend ID: ", friend_public_id)

    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""
            INSERT INTO public."Friends" (public_id, friend_public_id, friend_since)
            VALUES (%s, %s, %s)
            """,
                (current_user, friend_public_id, int(time.time()))
            )

            return jsonify({'message': 'friend added successfully'})



# TODO: ADD GETTING ALL FRIENDS LATEST LOCATION
@app.route("/api/get/latest_location", methods=['GET'])
@token_required
def get_latest_location(current_user):
    # SELECT * FROM public."LatestLocation" as loc, public."Friends"
    # WHERE loc.public_id='47e1422d-4eeb-4fe7-afd8-fc83888e7e21'

    
    with connection:
        with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM public."LatestLocation" WHERE public_id=%s
            """,
                (current_user,)
            )

            row = cursor.fetchone()

            print(datetime.datetime.utcnow())
            return jsonify({
                "time_fetched": int(time.time()),
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "time": row["time"],
            })




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")