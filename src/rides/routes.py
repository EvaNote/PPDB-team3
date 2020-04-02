from flask import Blueprint, flash, render_template, g, current_app, abort
from src.rides.forms import FindRideForm

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
    form = FindRideForm()
    if form.validate_on_submit():
        flash('You have been logged in successfully.', 'success')
    return render_template("findride.html", title="Find a ride", form=form)


@rides.route("/ride_info")
def ride_details():
    return render_template("ride_information.html", title="Ride information")


@rides.route("/ride_history")
def ride_history():
    return render_template("ride_history.html", title="Ride history")

@rides.route("/maps")
def maps():
    return render_template("maps.html", title="maps")
