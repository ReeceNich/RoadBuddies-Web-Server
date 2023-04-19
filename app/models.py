from datetime import date, datetime
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

# flask db init
# flask db stamp head  # usually need to run after changing db models (e.g., adding tables). see https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date
# flask db migrate -m "your changes"
# flask db upgrade

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    # id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)

    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64))
    email = db.Column(db.String(320), index=True, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # uselist - can only have one latest location.
    # latest_location = db.relationship("LatestLocation", uselist=False, backref="user")
    # friends_first = db.relationship("Friend", backref="user_first_id", primaryjoin="User.id==Friend.user_first_id")
    # friends_second = db.relationship("Friend", backref="user_second_id", primaryjoin="User.id==Friend.user_second_id")
    journeys = db.relationship("Journey", backref="journeys")


    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Friend(db.Model):
    user_first_id = db.Column(db.String(64), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True)
    user_second_id = db.Column(db.String(64), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True)
    # user_first_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True)
    # user_second_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True)
    
    is_friend = db.Column(db.Boolean, default=False, nullable=False)
    block_first_second = db.Column(db.Boolean, default=False, nullable=False)
    block_second_first = db.Column(db.Boolean, default=False, nullable=False)
    friend_requested = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    friend_since = db.Column(db.DateTime)

    def __repr__(self):
        return "<Friend {} and {} requested @ {}>".format(self.user_first_id, self.user_second_id, self.friend_requested)


# class LatestLocation(db.Model):
#     user_id = db.Column(db.String(64), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True, unique=True)
#     # user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True, unique=True)

#     latitude = db.Column(db.Float)
#     longitude = db.Column(db.Float)
#     time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     speed = db.Column(db.Float)

#     def __repr__(self):
#         return "<LatestLocation {} @ {}>".format(self.user_id, self.time)


class Journey(db.Model):
    journey_id = db.Column(db.String(64), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(64), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True)
    # journey_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    # user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="RESTRICT"), primary_key=True)

    time_started = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_ended = db.Column(db.DateTime)
    events = db.relationship("JourneyEvent", backref="events", cascade="all,delete")


    def __repr__(self):
        return "<Journey {} - User: {}>".format(self.journey_id, self.user_id)


class JourneyEvent(db.Model):
    journey_id = db.Column(db.String(64), db.ForeignKey("journey.journey_id", ondelete="CASCADE"), primary_key=True)
    event_id = db.Column(db.String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    # journey_id = db.Column(UUID(as_uuid=True), db.ForeignKey("journey.journey_id", ondelete="RESTRICT"), primary_key=True)
    # event_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    speed = db.Column(db.Float)
    is_speeding = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<JourneyEvent {} Event: {} @ {}>".format(self.journey_id, self.event_id, self.time)