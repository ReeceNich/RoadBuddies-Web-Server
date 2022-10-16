from datetime import datetime
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    public_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    # uselist - can only have one latest location.
    latest_location = db.relationship("LatestLocation", uselist=False, backref="user")

    def __repr__(self):
        return "<User {}>".format(self.username)


class LatestLocation(db.Model):
    public_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.public_id"), primary_key=True, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<LatestLocation {} - {}>".format(self.public_id, self.time)