from app import db
from app.models import User
from sqlalchemy import func


def test_add_user(app):
    with app.app_context():
        u1 = User(username="User1", email="user1@example.com", name="User 1")
        u1.set_password("u1")

        db.session.add(u1)
        db.session.commit()


        f1 = User.query.filter(func.lower(User.username) == func.lower("User1")).first()

        assert f1.username == "User1"
        assert f1.email == "user1@example.com"
        assert f1.name == "User 1"
        assert f1.check_password("u1") == True


def test_delete_user(app):
    test_add_user(app)

    with app.app_context():
        f1 = User.query.filter(func.lower(User.username) == func.lower("User1")).first()
        
        db.session.delete(f1)
        db.session.commit()

        f1 = User.query.filter(func.lower(User.username) == func.lower("User1")).first()

        assert f1 == None


def test_set_check_password():
    data = {"username": "User1", "password": "u1", "email": "user1@example.com", "name": "User 1"}

    u = data["username"] if "username" in data else None
    p = data["password"] if "password" in data else None
    e = data["email"] if "email" in data else None
    n = data["name"] if "name" in data else None

    u1 = User(username=u, email=e, name=n)
    u1.set_password(p)

    assert u1.check_password(p) == True
    assert u1.check_password("wrong") == False


def test_get_user_by_username(app):
    test_add_user(app)

    with app.app_context():
        u = "User1"
        u1 = User.query.filter(func.lower(User.username) == func.lower(u)).first()
        assert u1.username.lower() == u.lower()
        
        u = "user1"
        u1 = User.query.filter(func.lower(User.username) == func.lower(u)).first()
        assert u1.username.lower() == u.lower()

        u = "uSeR1"
        u1 = User.query.filter(func.lower(User.username) == func.lower(u)).first()
        assert u1.username.lower() == u.lower()


def test_get_user_by_email(app):
    test_add_user(app)

    with app.app_context():
        e = "user1@example.com"
        u1 = User.query.filter(func.lower(User.email) == func.lower(e)).first()
        assert u1.email.lower() == e.lower()
        
        e = "UsEr1@example.com"
        u1 = User.query.filter(func.lower(User.email) == func.lower(e)).first()
        assert u1.email.lower() == e.lower()
        
        e = "USER1@EXAMPLE.COM"
        u1 = User.query.filter(func.lower(User.email) == func.lower(e)).first()
        assert u1.email.lower() == e.lower()


def test_get_user_by_id(app):
    with app.app_context():
        u1 = User(id="userid", username="User1", email="user1@example.com", name="User 1")
        u1.set_password("u1")

        db.session.add(u1)
        db.session.commit()


        f1 = User.query.filter(func.lower(User.id) == func.lower("userid")).first()

        assert f1.username == "User1"
        assert f1.email == "user1@example.com"
        assert f1.name == "User 1"
        assert f1.check_password("u1") == True


def test_change_user_details(app):
    test_add_user(app)

    with app.app_context():
        f1 = User.query.filter(func.lower(User.username) == func.lower("user1")).first()
        uid = f1.id

        username = "New Username"
        name = "New Name"
        email = "newemail@example.com"
        password = "New Password"

        f1.username = username
        f1.name = name
        f1.email = email
        f1.set_password(password)

        db.session.commit()


        f2 = User.query.filter(func.lower(User.id) == func.lower(uid)).first()


        assert f2.check_password(password) == True
        assert f2.username == username
        assert f2.name == name
        assert f2.email == email