from flask import Blueprint, flash, render_template, g, current_app, abort
from flask_babel import lazy_gettext
from flask import Blueprint, flash, render_template, g, current_app, abort, redirect, url_for, request
from flask_login import current_user
import src.users.routes
from src.utils import user_access, car_access

rides = Blueprint('rides', __name__, url_prefix='/<lang_code>')


########################################################################################################################
# functions for multilingual support
@rides.url_defaults
def add_language_code(endpoint, values):
    if g.lang_code in current_app.config['SUPPORTED_LANGUAGES']:
        values.setdefault('lang_code', g.lang_code)
    else:
        values.setdefault('lang_code', 'en')


@rides.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@rides.before_request
def before_request():
    if g.lang_code not in current_app.config['SUPPORTED_LANGUAGES']:
        abort(404)


########################################################################################################################


@rides.route("/findride", methods=['GET', 'POST'])
def findride():
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    return render_template("findride.html", title=lazy_gettext("Find a ride"))


@rides.route("/createride", methods=['GET', 'POST'])
def createride():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("createride.html", title="Create a ride")


@rides.route("/ride_info")
def ride_details():
    return render_template("ride_information.html", title=lazy_gettext("Ride information"))


@rides.route("/ride_history")
def ride_history():
    return render_template("ride_history.html", title=lazy_gettext("Ride history"))


@rides.route("/maps")
def maps():
    return render_template("maps.html", title="maps")


@rides.route("/joinride", methods=['GET', 'POST'])
def joinride():
    return
