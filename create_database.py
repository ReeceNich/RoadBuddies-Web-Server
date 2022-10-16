from app import db, app
from app.models import User, LatestLocation

# flask db init
# flask db migrate -m "your changes"
# flask db upgrade

def new_db():
    db.drop_all()
    db.create_all()
    print("Dropped and created empty tables")

def add_example_users():

    u1 = User(username="User1", password="u1", email="user1@example.com", name="User 1")
    u2 = User(username="User2", password="u2", email="user2@example.com", name="User 2")
    u3 = User(username="User3", password="u3", email="user3@example.com", name="User 3")

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)

    db.session.commit()

    print("Added example users")


def add_example_latest_locations():
    u1 = LatestLocation(public_id=User.query.filter_by(username="User1").first().public_id, latitude=-50, longitude=1)
    u2 = LatestLocation(public_id=User.query.filter_by(username="User2").first().public_id, latitude=-51, longitude=2)
    u3 = LatestLocation(public_id=User.query.filter_by(username="User3").first().public_id, latitude=-52, longitude=3)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)

    db.session.commit()

    print("Added example latest locations")


with app.app_context():
    print("=== ARE YOU SURE YOU WANT TO RESET THE DATABASE? (y/n) ===")

    if(input().lower() == "y"):
        new_db()
        add_example_users()
        add_example_latest_locations()
        print("=== RESET THE DATABASE ===")

        u1 = User.query.filter_by(username="User1").first()
        print(u1.latest_location)