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
from itertools import groupby


# Creates a journey and returns the new journey ID.
@journey_bp.route("/", methods=['POST', 'GET'])
@token_required
def create_new_journey(current_user):
    if request.method == "POST":
        # Create a new journey.
        try:
            journey = request.get_json()
            # print("The POST data for Journey is:", journey)

            new = Journey(journey_id=journey["journey_id"],
                            user_id=current_user,
                            time_started=journey["time_started"],
                            time_ended=journey["time_ended"])

            db.session.add(new)
            db.session.commit()

            for event in journey["events"]:
                new = JourneyEvent(journey_id=event["journey_id"],
                                    event_id=event["event_id"],
                                    latitude=event["latitude"],
                                    longitude=event["longitude"],
                                    time=event["time"],
                                    speed=event["speed"],
                                    is_speeding=bool(event["is_speeding"]))

                db.session.add(new)
                db.session.commit()

            # db.session.commit()
            return jsonify({})
        
        except Exception as e:
            print("Journey Error", e)
            return make_response('could not create new journey',  400)
    else:
        # Return all journeys
        try:
            journeys = Journey.query.filter_by(user_id=current_user).join(JourneyEvent).order_by(Journey.time_started.desc(), JourneyEvent.time.desc()).all()
            journeys_list = []
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
    

# Returns a journey report to the current journey
@journey_bp.route("/report", methods=['POST'])
@token_required
def get_journey_report(current_user):
    try:
        data = request.get_json()
        journey = Journey.query.filter_by(journey_id=data["journey_id"]).join(JourneyEvent).order_by(Journey.time_started.desc(), JourneyEvent.time.desc()).first()

        report = {
            "journey_id": journey.journey_id,
            "total_distance": 0
        }


        for i in range(len(journey.events) - 1):
            report["total_distance"] += haversine(journey.events[i].latitude, journey.events[i].longitude,
                                                  journey.events[i+1].latitude, journey.events[i+1].longitude)

        
        # for i in range(len(journey.events)):
        #     if journey.events[i].is_speeding:
        #         report["speeding_count"] += 1
        # else:
        #     report["speeding_count_percentage"] = (report["speeding_count"] / len(journey.events)) * 100


        # Count the number of different speeding violations.
        speeding_percentage = 0
        speeding_violations = 0
        speeding_locations = []
        for key, group in groupby(journey.events, key=lambda x: x.is_speeding):
            if key == True:
                events = list(group)
                group_length = len(events)
                if group_length >= 2:
                    speeding_percentage += group_length
                    speeding_violations += 1
                    
                    locs = []
                    for event in events:
                        locs.append({"latitude": event.latitude,
                                     "longitude": event.longitude,
                                     "speed": event.speed})
                    
                    speeding_locations.append(locs)
        
        report["speeding_percentage"] = (speeding_percentage / len(journey.events)) * 100
        report["speeding_separate_violations"] = speeding_violations
        report["speeding_locations"] = speeding_locations
        
        
        print("Report:", report)

        return jsonify(report)

    except Exception as e:
        print(e)
        return make_response('could not generate journey report',  400)
    



# Calculate the distance between two coordinates.

from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c
    return d * 1000