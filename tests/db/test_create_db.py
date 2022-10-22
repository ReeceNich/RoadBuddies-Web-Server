from config import TestConfig
from app import db
# from app.models import User
# from sqlalchemy import func


def test_config(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"]


def test_create_db(app):
    TABLES = ["user", "friend", "latest_location", "journey", "journey_event"]
    
    with app.app_context():
        db.create_all()
        db.drop_all()
        
        keys = db.metadata.tables.keys()

        assert len(keys) == len(TABLES)

        for i in list(keys):
            assert (i in TABLES) == True
