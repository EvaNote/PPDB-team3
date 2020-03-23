from flask import Flask
from flask_babel import Babel
from src.config import *
from src.models import *
# import blueprints
from src.main.routes import main
from src.reviews.routes import reviews
from src.rides.routes import rides
from src.users.routes import users

# connect to database
connection = DBConnection(dbname=BaseConfig.DB_NAME, dbuser=BaseConfig.DB_USER)
user_access = UserAccess(connection)
# create Babel extension which is used for making our app multilingual
babel = Babel()


def create_app(config_class=BaseConfig):
    """
    Create a Flask application with a given configuration. This function allows us to create
    multiple instances of our app with different configurations.
    :param config_class: the object used to configurate the Flask application
    :return: configured Flask app
    """
    # setup Flask app
    app = Flask(__name__)
    # load configuration from a certain Config class in config.py
    app.config.from_object(config_class)
    # register blueprints into the app
    app.register_blueprint(main)
    app.register_blueprint(reviews)
    app.register_blueprint(rides)
    app.register_blueprint(users)
    # initialize extensions with the app
    babel.init_app(app)
    return app
