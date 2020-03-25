class BaseConfig(object):
    """
    Base configuration class with variables used in the creation of our Flask
    app and database connection.
    """
    # general
    SECRET_KEY = 'ce6593aceb62762cb4d3537c96100349'

    # babel
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    SUPPORTED_LANGUAGES = {'en': 'English', 'nl': 'Nederlands', 'fr': 'Français'}

    # database
    DB_USER = 'app'
    DB_NAME = 'dbcarpool'


class ProductionConfig(BaseConfig):
    """ Configuration used for deploying our app in production. """
    ENV = 'production'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """ Configuration used for development purposes. """
    ENV = 'development'
    DEBUG = True
    TESTING = False


class TestConfig(BaseConfig):
    """ Configuration used for running tests. """
    ENV = 'development'
    DEBUG = True
    TESTING = True
