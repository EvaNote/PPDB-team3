from flask import Blueprint, flash, render_template, g, current_app, abort
from src.rides.forms import FindRideForm
from flask_babel import lazy_gettext
from flask import Blueprint, flash, render_template, g, current_app, abort, redirect, url_for, request
from flask_login import current_user
from src.rides.forms import FindRideForm, CreateRideForm
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
    form = FindRideForm()
    if form.validate_on_submit():
        flash('You have been logged in successfully.', 'success')
    return render_template("findride.html", title=lazy_gettext("Find a ride"), form=form)

@rides.route("/createride", methods=['GET', 'POST'])
def createride():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = CreateRideForm()
    cars_list = list()

    if form.validate_on_submit():
        fromField = form.fromField.data
        toField = form.toField.data
        date = form.Date.data
        time = form.Time.data

        user = user_access.get_user_on_id(current_user.id)
        cars = car_access.get_on_user_id(user.id)
        for car in cars:
            string = car.brand + " " + car.model
            cars_list.append(string)

        flash('Created a ride.', 'success')
        return redirect(url_for('users.myrides'))
    return render_template("createride.html", title="Create a ride", form=form, cars=cars_list)


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
