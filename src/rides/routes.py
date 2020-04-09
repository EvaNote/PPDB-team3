from flask import Blueprint, flash, render_template, g, current_app, abort, redirect, url_for, request
from flask_login import current_user
from src.rides.forms import FindRideForm, CreateRideForm
import src.users.routes

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

@rides.route("/createride", methods=['GET', 'POST'])
def createride():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = CreateRideForm()
    if form.validate_on_submit():
        fromField = form.fromField.data
        toField = form.toField.data
        date = form.Date.data
        time = form.Time.data

        flash('Created a ride.', 'success')
        return redirect(url_for('users.myrides'))
    return render_template("createride.html", title="Create a ride", form=form)

@rides.route("/ride_info")
def ride_details():
    return render_template("ride_information.html", title="Ride information")


@rides.route("/ride_history")
def ride_history():
    return render_template("ride_history.html", title="Ride history")

@rides.route("/maps")
def maps():
    return render_template("maps.html", title="maps")
