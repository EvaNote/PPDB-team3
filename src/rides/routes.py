from flask import Blueprint, flash, render_template, g, current_app, abort
from flask_babel import lazy_gettext
from flask import Blueprint, flash, render_template, g, current_app, abort, redirect, url_for, request
from flask_login import current_user
import src.users.routes
from src.rides.forms import Filter_rides
from src.utils import user_access, car_access, ride_access, picture_access, pickup_point_access, address_access, campus_access
from src.emails import *

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
    form = Filter_rides()
    return render_template("ride_history.html", title=lazy_gettext("Ride history"), form=form)


@rides.route("/view_ride=<rideid>", methods=['GET', 'POST'])
def view_ride(rideid):
    if not rideid.isdigit():
        abort(404)
    loggedIn = current_user.is_authenticated
    allrides_temp = ride_access.get_on_id(int(rideid))
    if allrides_temp is None:
        abort(404)
    allrides = []
    allrides.append(allrides_temp)
    if allrides is None:
        allrides = []
    userrides = []
    from_places = []
    to_places = []
    from_lat = []
    from_lng = []
    to_lat = []
    to_lng = []
    pfps = []
    allids = []
    pickuppoints = []
    pickupbools = []
    for ride in allrides:
        userrides.append(ride)
        if ride.campus_from:
            from_places.append(ride.campus_from.name)
        else:
            temp = ride.address_from
            from_places.append(temp.city + ", " + temp.street + ", " + temp.nr)
        if ride.campus_to:
            to_places.append(ride.campus_to.name)
        else:
            temp = ride.address_to
            to_places.append(temp.city + ", " + temp.street + ", " + temp.nr)
        from_lat.append(ride.address_from.latitude)
        from_lng.append(ride.address_from.longitude)
        to_lat.append(ride.address_to.latitude)
        to_lng.append(ride.address_to.longitude)
        temp = list(ride_access.get_passenger_ids(ride.id))
        temp2 = []
        ride_pfp = []
        userids = []
        points = []
        bools = [False,False,False]

        for user_id in temp:
            if not loggedIn or user_id is not current_user.id:
                temp2.append(user_id)
                # userids.append(user_id)
                user = user_access.get_user_on_id(user_id)
                # if user.picture is not None:
                #     ride_pfp.append("images/" + str(picture_access.get_picture_on_id(user.picture).filename))
                # else:
                #     ride_pfp.append("images/temp_profile_pic.png")
        temp2.append(ride.user_id)
        #userids.append(user_id)
        user = user_access.get_user_on_id(ride.user_id)

        if user.picture is not None:
            pfps.append("images/" + str(picture_access.get_picture_on_id(user.picture).filename))
        else:
            pfps.append("images/temp_profile_pic.png")

        allids.append(temp2)
        #pfps.append(ride_pfp)
        if ride.pickup_1 is not None:
            pickup_1_id = ride.pickup_1
            time_1 = pickup_point_access.get_on_id(pickup_1_id).estimated_time
            points.append(time_1)
            bools[0] = True
            if ride.pickup_2 is not None:
                pickup_2_id = ride.pickup_2
                time_2 = pickup_point_access.get_on_id(pickup_2_id).estimated_time
                points.append(time_2)
                bools[1] = True
                if ride.pickup_3 is not None:
                    pickup_3_id = ride.pickup_3
                    time_3 = pickup_point_access.get_on_id(pickup_3_id).estimated_time
                    points.append(time_3)
                    bools[2] = True
        pickupbools.append(bools)
        pickuppoints.append(points)

    return render_template('ride.html', title=lazy_gettext('Joined rides'),
                           loggedIn=True,
                           userrides=list(userrides),
                           pickuppoints=list(pickuppoints),
                           pickupbools=list(pickupbools),
                           from_locs=list(from_places),
                           to_locs=list(to_places),
                           pfps=list(pfps),
                           rideid=rideid,
                           from_lat=list(from_lat),
                           from_lng=list(from_lng),
                           to_lat=list(to_lat),
                           to_lng=list(to_lng))

# @rides.route("/maps")
# def maps():
#     return render_template("maps.html", title="maps")

@rides.route("/join=<rideid>")
def join(rideid):
    if not rideid.isdigit:
        abort(404)
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    result = ride_access.register_passenger(current_user.id, rideid)
    if result:
        flash('joined ride.', 'success')
        return redirect(url_for("main.home"))
    else:
        flash('Could not join ride.', 'danger')
        return redirect(url_for("rides.view_ride", rideid=rideid))


@rides.route("/joinride", methods=['GET', 'POST'])
def joinride():
    ride_id = request.json.get("ride_id")
    ride = ride_access.get_on_id(ride_id)
    if ride.user_id == current_user.id:
        return {"result": "current user is driver"}

    result = ride_access.register_passenger(current_user.id, ride_id)
    driver_id = ride.user_id
    driver = user_access.get_user_on_id(driver_id)
    passenger = user_access.get_user_on_id(current_user.id)
    passenger_name = passenger.first_name + " " + passenger.last_name
    if ride.campus_to_id() is None:
        dest = ride.address_to
        destination = dest.street + " " + dest.nr + ", " + dest.city
    else:
        dest = campus_access.get_on_id(ride.campus_to_id())
        destination = dest.name

    if result:
        if driver.send_emails is True:
            send_email_newpassenger(driver.email, passenger_name, str(ride.departure_time), destination)
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