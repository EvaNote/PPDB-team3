from flask import Flask, g, request, redirect, url_for
from src.models import UserAccess
from src.config import *
from src.utils import babel, bcrypt, login_manager
# import all blueprints
from src.main.routes import main
from src.reviews.routes import reviews
from src.rides.routes import rides
from src.users.routes import users


def create_app(config_class=BaseConfig):
    """
    Create a Flask application with a given configuration. This function allows us to create
    multiple instances of our app with different configurations.
    :param config_class: the object used to configurate the Flask application
    :return: configured Flask app
    """

    def redirect_root_to_home():
        """
        This helper function is used to redirect the root URL (team3.ppdb.me) to the home page
        in the language that matches best for the current user (i.e. team3.ppdb.me/en/home).
        """
        g.lang_code = request.accept_languages.best_match(BaseConfig.SUPPORTED_LANGUAGES)
        return redirect(url_for('main.home'))

    # setup Flask app
    app = Flask(__name__)
    # load configuration from a certain Config class in config.py
    app.config.from_object(config_class)
    # register blueprints into the app
    app.register_blueprint(main)
    app.register_blueprint(reviews)
    app.register_blueprint(rides)
    app.register_blueprint(users)
    app.add_url_rule('/', 'home', redirect_root_to_home)
    # initialize extensions with the app
    babel.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    return app
