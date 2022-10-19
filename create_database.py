from app import db, app
from app.models import User, Friend, LatestLocation

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

    # db.session.add([u1, u2, u3])
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.commit()

    print("Added example users")


def add_example_latest_locations():
    u1 = LatestLocation(user_id=User.query.filter_by(username="User1").first().id, latitude=-50, longitude=1)
    u2 = LatestLocation(user_id=User.query.filter_by(username="User2").first().id, latitude=-51, longitude=2)
    u3 = LatestLocation(user_id=User.query.filter_by(username="User3").first().id, latitude=-52, longitude=3)

    # db.session.add([u1, u2, u3])
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.commit()

    print("Added example latest locations")


def add_example_friends():
    f1 = Friend(user_first_id=User.query.filter_by(username="User1").first().id,
            user_second_id=User.query.filter_by(username="User2").first().id)

    db.session.add(f1)
    db.session.commit()

with app.app_context():

    if(input("=== ARE YOU SURE YOU WANT TO RESET THE DATABASE? (y/n) ===").lower() == "y"):
        new_db()
        add_example_users()
        add_example_latest_locations()
        add_example_friends()

        print("=== RESET THE DATABASE ===")

        # u1 = User.query.filter_by(username="User1").first()
        # print(u1.latest_location)
    

    if(input("Do you want to view friends relationships? (y/n) ").lower() == "y"):
        f1 = Friend.query.filter_by(user_first_id=User.query.filter_by(username="User1").first().id).all()

        print(f1)

        print("added example friends relationships")