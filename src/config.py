class TheConfig:
    config = None


def set_config(config):
    TheConfig.config = config


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


class ProductionConfig(BaseConfig):
    """ Configuration used for deploying our app in production. """
    ENV = 'production'
    DEBUG = False
    TESTING = False

    # database
    DB_USER = 'app'
    DB_NAME = 'dbcarpool'


class DevelopmentConfig(BaseConfig):
    """ Configuration used for development purposes. """
    ENV = 'development'
    DEBUG = True
    TESTING = False

    # database
    DB_USER = 'app'
    DB_NAME = 'dbcarpool'


class TestConfig(BaseConfig):
    """ Configuration used for running tests. """
    ENV = 'development'
    DEBUG = True
    TESTING = True

    # database
    DB_USER = 'app'
    DB_NAME = 'dbcarpool_test'
