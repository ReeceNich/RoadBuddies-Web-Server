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
from app.models import User, LatestLocation, Friend
from sqlalchemy import func
from app.users import users_bp
from app.routes import token_required


@users_bp.route('/login', methods=['POST']) 
def login_user():
    auth = request.authorization  
    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify auth headers', 401, {'Authentication': 'login required"'})   


    # TODO: CHANGE THIS QUERY TO POSTGRES
    user = User.query.filter(func.lower(User.username) == func.lower(auth.username)).first()

    # with connection:
    #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
    #         print("AUTHHH: ", auth.username, auth.password)
    #         cursor.execute('SELECT * FROM public."user" WHERE LOWER(username)=LOWER(%s)', (auth.username,))

    #         user = cursor.fetchone()
    #         print("Login User Row: ", user)

    # if check_password_hash(user["password"], auth.password):

    if user.check_password(auth.password):
        token = jwt.encode({'id' : str(user.id), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=525960)}, current_app.config['SECRET_KEY'], "HS256")

        return jsonify({'token' : token})



    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@users_bp.route('/register', methods=['POST'])
def signup_user(): 
    data = request.get_json() 
    # hashed_password = generate_password_hash(data['password'], method='sha256')

    # TODO: CHANGE THIS QUERY TO POSTGRES
    # new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    # db.session.add(new_user) 
    # db.session.commit()

    

    # with connection:
    #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
    #         cursor.execute('INSERT INTO public."user" (id, username, password, email, name) VALUES (%s, %s, %s, %s, %s)',
    #             (str(uuid.uuid4()), data["username"], hashed_password, data["email"], data["name"]))

    try:
        new_user = User(id=str(uuid.uuid4()), username=data["username"], name=data["name"], email=data["email"])
        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'registered successfully'})
    except:
        return make_response('registration unsuccessful', 400)


@users_bp.route('/', methods=['GET'])
@token_required
def get_user_info(current_user):
    
    # with connection:
    #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
    #         cursor.execute('SELECT * FROM public."User" WHERE public_id=%s', (current_user,))

    #         user = cursor.fetchone()
    #         print("Get User Info Row: ", user)

    try:
        user = User.query.filter_by(id=current_user).first()
            
        return jsonify({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "created": user.created
        })
    except:
        return make_response('Could not get user information',  400)


def get_id_from_username(username):
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    return user.id

    # with connection:
    #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
    #         cursor.execute('SELECT public_id FROM public."User" WHERE username=%s', (username,))

    #         user = cursor.fetchone()
    #         return user["public_id"]


# TODO: Add error handling for existing friend.
@users_bp.route("/add/friend", methods=['POST'])
@token_required
def add_friend(current_user):
    data = request.get_json()



    try:
        friend_id = get_id_from_username(data["friend_username"])

        print("Friend ID: ", friend_id)
        rel = Friend(user_first_id=current_user, user_second_id=friend_id)
        db.session.add(rel)
        db.session.commit()
        return jsonify({'message': 'friend added successfully'})

    except:
        return make_response('could not add friend',  400)



    # with connection:
    #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
    #         cursor.execute("""
    #         INSERT INTO public."Friends" (public_id, friend_public_id, friend_since)
    #         VALUES (%s, %s, %s)
    #         """,
    #             (current_user, friend_public_id, int(time.time()))
    #         )


# @users_bp.route("/add/latest_location", methods=['POST'])
# @token_required
# def add_latest_location(current_user):
#     data = request.get_json() 
#     print(data)

#     # TODO: get time from the user request, but make sure it is proper timestamp
#     try:    
#         current = LatestLocation.query.filter_by(user_id=current_user).first()


#         if current:
#             print("Yes")

#             # current.latitude = data.get("latitude", None)
#             current.latitude = data["latitude"] if "latitude" in data else None
#             current.longitude = data["longitude"] if "longitude" in data else None
#             current.speed = data["speed"] if "speed" in data else None
#             current.time = data["time"] if "time" in data else datetime.datetime.utcnow()

#             db.session.commit()
#         else:
#             print("No")

#             ll = LatestLocation(user_id=current_user, latitude=data.get("latitude", None), longitude=data.get("longitude", None), speed=data.get("speed", None), time=data.get("time", datetime.datetime.utcnow()))

#             db.session.add(ll)
#             db.session.commit()
 
#         return jsonify({'message': 'location updated successfully'})
#     except Exception as e:
#         print(e)
#         return make_response('could not update location',  400)


    # with connection:
    #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
    #         cursor.execute("""
    #         INSERT INTO public."LatestLocation" (public_id, latitude, longitude, time)
    #         VALUES (%s, %s, %s, %s)
    #         ON CONFLICT(public_id) DO UPDATE
    #         SET latitude = excluded.latitude,
    #             longitude = excluded.longitude,
    #             time = excluded.time
    #         """,
    #             (current_user, data["latitude"], data["longitude"], data["time"])
    #         )
    #         return jsonify({'message': 'location updated successfully'})


# # TODO: ADD GETTING ALL FRIENDS LATEST LOCATION
# @users_bp.route("/get/latest_location", methods=['GET'])
# @token_required
# def get_latest_location(current_user):
#     # SELECT * FROM public."LatestLocation" as loc, public."Friends"
#     # WHERE loc.public_id='47e1422d-4eeb-4fe7-afd8-fc83888e7e21'

#     loc = LatestLocation.query.filter_by(user_id=current_user).first()

#     return jsonify({
#                 "time_fetched": datetime.datetime.utcnow(),
#                 "latitude": loc.latitude,
#                 "longitude": loc.longitude,
#                 "time": loc.time
#             })
    
#     # with connection:
#     #     with connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cursor:
#     #         cursor.execute("""
#     #             SELECT * FROM public."LatestLocation" WHERE public_id=%s
#     #         """,
#     #             (current_user,)
#     #         )

#     #         row = cursor.fetchone()

#     #         print(datetime.datetime.utcnow())
            
