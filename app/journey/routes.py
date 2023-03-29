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
from app.models import User, Journey, JourneyEvent
from sqlalchemy import func
from app.journey import journey_bp
from app.routes import token_required


# Creates a journey and returns the new journey ID.
@journey_bp.route("/", methods=['POST', 'GET'])
@token_required
def create_new_journey(current_user):
    if request.method == "POST":
        # Create a new journey.
        try:
            new = Journey(user_id=current_user, time_started=datetime.datetime.utcnow())

            db.session.add(new)
            db.session.commit()
            
            return jsonify({"journey_id": new.journey_id,
                            "user_id": new.user_id,
                            "time_started": new.time_started})
        
        except Exception as e:
            print(e)
            return make_response('could not create new journey',  400)
    else:
        # Return all journeys
        try:
            journeys = Journey.query.filter_by(user_id=current_user).join(JourneyEvent).order_by(Journey.time_started.desc(), JourneyEvent.time.desc()).all()
            journeys_list = []
            print(journeys)
            for journey in journeys:
                journey_dict = {
                    "journey_id": journey.journey_id,
                    "user_id": journey.user_id,
                    "time_started": journey.time_started,
                    "time_ended": journey.time_ended,
                    "events": []
                }
                for event in journey.events:
                    event_dict = {
                        "journey_id": event.journey_id,
                        "event_id": event.event_id,
                        "latitude": event.latitude,
                        "longitude": event.longitude,
                        "time": event.time,
                        "speed": event.speed,
                        "is_speeding": event.is_speeding
                    }
                    journey_dict["events"].append(event_dict)
                journeys_list.append(journey_dict)


            print(journeys_list)
            return jsonify(journeys_list)

        except Exception as e:
            print(e)
            return make_response('could not return all journeys',  400)


# Ends a journey and returns the new journey ID.
@journey_bp.route("/end", methods=['POST'])
@token_required
def end_journey(current_user):
    try:
        data = request.get_json()

        journey = Journey.query.filter_by(journey_id=data["journey_id"]).first()

        journey.time_ended = datetime.datetime.utcnow()

        db.session.commit()
 
        return jsonify({"journey_id": journey.journey_id,
                        "user_id": journey.user_id,
                        "time_started": journey.time_started,
                        "time_ended": journey.time_ended})
    
    except Exception as e:
        print(e)
        return make_response('could not create new journey',  400)




# Adds an event to the current journey
@journey_bp.route("/event/", methods=['POST'])
@token_required
def create_new_event(current_user):
    data = request.get_json()

    try:
        new = JourneyEvent(journey_id=data["journey_id"],
                           latitude=data["latitude"],
                           longitude=data["longitude"],
                           time=datetime.datetime.utcnow(),
                           speed=data["speed"],
                           is_speeding=bool(data["is_speeding"]))

        db.session.add(new)
        db.session.commit()
 
        return jsonify({"journey_id": new.journey_id,
                        "event_id": new.event_id,
                        "latitude": new.latitude,
                        "longitude": new.longitude,
                        "time": new.time,
                        "speed": new.speed,
                        "is_speeding": new.is_speeding})
    
    except Exception as e:
        print(e)
        return make_response('could not add new event',  400)