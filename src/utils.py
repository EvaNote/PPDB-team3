from flask import g, current_app
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from geopy.geocoders import Nominatim
from src.DBConnect import DBConnection
from src.dbmodels.Address import Addresses
from src.dbmodels.Campus import Campusses
from src.dbmodels.Car import Cars
from src.dbmodels.Picture import Pictures
from src.dbmodels.Review import Reviews
from src.dbmodels.Ride import Rides
from src.dbmodels.User import UserAccess
from src.config import BaseConfig

# connect to database
connection = DBConnection(dbname=BaseConfig.DB_NAME, dbuser=BaseConfig.DB_USER)
address_access = Addresses(connection)
campus_access = Campusses(connection)
car_access = Cars(connection)
picture_access = Pictures(connection)
review_access = Reviews(connection)
ride_access = Rides(connection)
user_access = UserAccess(connection)

# create extensions
babel = Babel()
bcrypt = Bcrypt()
login_manager = LoginManager()
geolocator = Nominatim(user_agent="dbcarpool")


# source: https://flask-user.readthedocs.io/en/v0.6/internationalization.html
@babel.localeselector
def get_locale():
    """ Use the browser's language preferences to select an available translation """
    return g.get('lang_code', current_app.config['BABEL_DEFAULT_LOCALE'])


@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone


@login_manager.user_loader
def load_user(user_id):
    return UserAccess(connection).get_user_on_id(user_id)
