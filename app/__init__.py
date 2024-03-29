from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
def create_app(config_class=Config):
    app = Flask(__name__)
    # gets variables from environment
    # app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app, db)

    from app.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    from app.journey import journey_bp
    app.register_blueprint(journey_bp, url_prefix="/api/journey")

    return app

# TODO: MIGHT NOT NEED THIS IMPORT ANYMORE
# from app import models
