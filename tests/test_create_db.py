import pytest
from config import TestConfig
from app import db
from app.models import User

def test_config(app):
    assert TestConfig.SQLALCHEMY_DATABASE_URI == "sqlite:///"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///"



def test_create_db(app):
    TABLES = ["user", "friend", "latest_location", "journey", "journey_event"]
    
    with app.app_context():
        db.create_all()
        
        keys = db.metadata.tables.keys()

        assert len(keys) == len(TABLES)

        for i in list(keys):
            assert (i in TABLES) == True
    

def test_add_user(app):
    with app.app_context():
        u1 = User(username="User1", email="user1@example.com", name="User 1")
        u1.set_password("u1")

        db.session.add(u1)
        db.session.commit()


        f1 = User.query.filter_by(username="User1").first()

        assert f1.username == "User1"
        assert f1.email == "user1@example.com"
        assert f1.name == "User 1"
        assert f1.check_password("u1") == True