import pytest
from app import create_app, db
from config import TestConfig


# Creates a flask "app" variable which can be passed as a parameter into the test functions.
@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    return app

