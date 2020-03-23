from flask import Blueprint, flash, render_template
from src.rides.forms import FindRideForm

rides = Blueprint('rides', __name__)


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
