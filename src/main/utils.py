from flask import g
from src import babel


# source: https://damyanon.net/post/flask-series-internationalization/
@babel.localeselector
def get_locale():
    # try to get browser language code
    return g.get('lang_code', )


@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone
