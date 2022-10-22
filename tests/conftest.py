import pytest
from app import create_app, db
from config import TestConfig, TestProdConfig


# Creates a flask "app" variable which can be passed as a parameter into the test functions.
# Note: The fixture runs every time it is called (e.g., the app is created every time and the database is recreated every time).
# By using a yield statement instead of return, all the code after the yield statement serves as the teardown code.
@pytest.fixture
def app():
    app = create_app(TestConfig)
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    # return app


# Test client makes requests to the application without running a live server
@pytest.fixture()
def client(app):
    return app.test_client()