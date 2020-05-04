from flask import Blueprint, flash, render_template, g, current_app, abort
from flask_babel import lazy_gettext
from flask import Blueprint, flash, render_template, g, current_app, abort, redirect, url_for, request
from flask_login import current_user
import src.users.routes
from src.utils import user_access, car_access, ride_access

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
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    return render_template("createride.html", title="Create a ride")


@rides.route("/ride_info")
def ride_details():
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    return render_template("ride_information.html", title=lazy_gettext("Ride information"))


@rides.route("/ride_history")
def ride_history():
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    return render_template("ride_history.html", title=lazy_gettext("Ride history"))


# @rides.route("/maps")
# def maps():
#     return render_template("maps.html", title="maps")


@rides.route("/joinride", methods=['GET', 'POST'])
def joinride():
    ride_id = request.json.get("ride_id")
    result = ride_access.register_passenger(current_user.id, ride_id)
    if result:
        return {"result": "success"}
    return {"result": "failed"}

#TODO
#
# @rides.route("/edit_ride=<rideid>",methods=['GET', 'POST'])
# def edit_ride(rideid):
#     if not rideid.isdigit():
#         abort(404)
#     form = Reviews()
#     target_user = user_access.get_user_on_id(userid)
#     form2 = SelectSubject()
#
#     pfp_path = "images/"
#     if target_user.picture is not None:
#         pfp_path += picture_access.get_picture_on_id(target_user.picture).filename
#     else:
#         pfp_path += "temp_profile_pic.png"
#
#     if form2.validate_on_submit() and current_user.is_authenticated:
#         user = user_access.get_user_on_id(current_user.id)
#         subject = lazy_gettext('Campus Carpool: user message')
#         message = lazy_gettext('Dear ') + target_user.first_name + ' ' + target_user.last_name + '\n'
#         if form2.subject.data == 'Empty':
#             pass
#         elif form2.subject.data == 'Lost item':
#             subject += lazy_gettext(": Lost item")
#             message += lazy_gettext(
#                 "While carpooling with you recently, I forgot my [ITEM] in your car. Can you let me know if you found it and when you can return it?")
#         message += lazy_gettext('\nKind regards\n') + user.first_name + ' ' + user.last_name
#         return redirect('mailto:' + target_user.email + '?SUBJECT=' + subject + '&BODY=' + message)
#     cars = car_access.get_on_user_id(userid)
#     data = review_access.get_on_user_for(userid)
#     car_picpaths = []
#     if cars == None:
#         cars = []
#     for car in cars:
#         if car.picture is None:
#             car_picpaths.append("images/temp_car_pic.jpg")
#         else:
#             car_picpaths.append("images/" + picture_access.get_picture_on_id(car.picture).filename)
#     return render_template('user.html', title=lazy_gettext('User profile'), form=form, loggedIn=False,
#                            target_user=target_user,
#                            data=data, cars=cars, form2=form2, pfp_path=pfp_path, car_picpaths=car_picpaths)