from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort, request
from pathlib import Path
import secrets
import os
from PIL import Image
from flask_login import current_user, login_user, logout_user
from src.dbmodels.User import User
from src.dbmodels.Car import Car
from src.dbmodels.Address import Address
from src.dbmodels.Picture import Picture
from src.reviews.forms import Reviews
from src.dbmodels.PickupPoint import PickupPoint
from src.users.forms import LoginForm, RegistrationForm, VehicleForm, EditAccountForm, EditAddressForm, SelectSubject, \
    DeleteUserForm, getCalendar
from src.rides.forms import Filter_rides
from src.utils import user_access, bcrypt, review_access, car_access, address_access, current_app, picture_access, ride_access, campus_access, \
    geolocator, pickup_point_access
from flask_babel import lazy_gettext
from math import floor
from ics import Calendar, Event
from datetime import *
from copy import deepcopy
from src.emails import *

users = Blueprint('users', __name__, url_prefix='/<lang_code>')


########################################################################################################################
# functions for multilingual support
@users.url_defaults
def add_language_code(endpoint, values):
    if g.lang_code in current_app.config['SUPPORTED_LANGUAGES']:
        values.setdefault('lang_code', g.lang_code)
    else:
        values.setdefault('lang_code', 'en')


@users.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@users.before_request
def before_request():
    if g.lang_code not in current_app.config['SUPPORTED_LANGUAGES']:
        abort(404)


########################################################################################################################

def makeEvent(ride, isDriver):
    e = Event()
    if isDriver:
        e.name = "Campus Carpool: " + lazy_gettext("driver")
    else:
        e.name = "Campus Carpool: " + lazy_gettext("passenger")
    e.begin = ride.departure_time
    e.end = ride.arrival_time
    e.created = datetime.now()
    locString = ""
    if ride.campus_from:
        locString += ride.campus_from.name
    else:
        address = ride.address_from
        locString += address.street + " " + str(address.nr) + ", " + address.city + " - "
    if ride.campus_to:
        locString += ride.campus_to.name
    else:
        address = ride.address_to
        locString += address.street + " " + str(address.nr) + ", " + address.city
    if isDriver:
        e.location = locString
        driver = user_access.get_user_on_id(ride.user_id)
        locString += "\\n" + driver.first_name + " " + driver.last_name
        e.description = locString
    else:
        e.location = locString
        locString += "\\n" + str(ride.passengers) + " passengers"
        e.description = locString
    # TODO: naam bestuurder?
    return e

def generate_calendar(user_id):
    # From https://pypi.org/project/ics/
    c = Calendar()

    driver_for = ride_access.get_on_user_id(user_id)
    passenger_for = ride_access.get_rides_from_passenger(user_id)

    if driver_for is not None:
        for ride in driver_for:
            e = makeEvent(ride,True)
            c.events.add(e)

    if passenger_for is not None:
        for ride in passenger_for:
            e = makeEvent(ride,False)
            c.events.add(e)

    cal_name = "cal" + str(user_id) + ".ics"
    #filename/path
    path = Path(users.root_path)
    path = path.parent
    cal_path = os.path.join(path, 'static/ics', cal_name)

    with open(cal_path, 'w') as my_file:
        my_file.writelines(c)
    return


@users.route("/account", methods=['GET', 'POST'])
def account():
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))

    calForm = getCalendar()
    form = Reviews()
    user = current_user
    if current_app.config['TESTING']:
        user = user_access.get_user_on_id(1)
    data = review_access.get_on_user_for(user.id)
    cars = car_access.get_on_user_id(user.id)
    user = user_access.get_user_on_id(user.id)
    address = address_access.get_on_id(user.address)
    car_picpaths = []
    if cars == None:
        cars = []
    for car in cars:
        if car.picture is None:
            car_picpaths.append("images/temp_car_pic.jpg")
        else:
            car_picpaths.append("images/" + picture_access.get_picture_on_id(car.picture).filename)

    pfp_path = "images/"
    if user.picture is not None:
        pfp_path += picture_access.get_picture_on_id(user.picture).filename
    else:
        pfp_path += "temp_profile_pic.png"

    rev_pfps = []
    mean = 0
    reviews = 0
    for review in data:
        user2 = user_access.get_user_on_id(review.user_from)
        if user2.picture is not None:
            rev_pfps.append("images/" + picture_access.get_picture_on_id(user2.picture).filename)
        else:
            rev_pfps.append("images/temp_profile_pic.png")
        mean += review.amount_of_stars
        reviews += 1
    if reviews > 0:
        mean = mean / reviews

    whole_stars = floor(mean)
    if mean - whole_stars >= 0.3:
        half_stars = 1
    else:
        half_stars = 0

    if calForm.submit.data:
        # Generate calendar file, give link
        generate_calendar(current_user.id)
        path = "ics/cal" + str(current_user.id) + ".ics"
        file_url = url_for('static', filename=path)
        #TODO, als iemand hier echt veel zin in heeft
        #redirect_url = "webcal:/" + file_url
        return redirect(file_url)

    return render_template('account.html', title=lazy_gettext('Account'), form=form, loggedIn=True, data=data,
                           current_user=user, cars=cars, address=address, carPicpaths=car_picpaths, pfp_path=pfp_path,
                           car_picpaths=car_picpaths, target_user=user, rev_pfps=rev_pfps, mean_rate=mean,
                           half_stars=half_stars, whole_stars=whole_stars, calForm=calForm)


# van https://www.youtube.com/watch?v=803Ei2Sq-Zs
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # van https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    path = Path(users.root_path)
    path = path.parent
    picture_path = os.path.join(path, 'static/images', picture_fn)
    output_size = (127, 127)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@users.route("/edit", methods=['GET', 'POST'])
def account_edit():
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    form = EditAccountForm()
    if request.method != 'POST':
        if current_app.config['TESTING']:
            user = user_access.get_user_on_id(1)
        else:
            user = user_access.get_user_on_id(current_user.id)
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.gender.data = user.gender
        form.age.data = user.age
        form.phone_number.data = user.phone_number
        if user.send_emails is True:
            form.send_emails.data = True
        else:
            form.send_emails.data = False

        return render_template('account_edit.html', title=lazy_gettext('Edit account info'), loggedIn=True, form=form)
    if form.validate_on_submit():
        if form.submit.data:
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            gender = form.gender.data
            age = form.age.data
            phone_number = form.phone_number.data
            user = user_access.get_user_on_id(current_user.id)
            picture_id = user.picture
            send_emails = form.send_emails.data
            if send_emails is True:
                send_emails_data = 'TRUE'
            else:
                send_emails_data = 'FALSE'

            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                picture_obj = Picture(None, filename=picture_file)
                picture_access.add_picture(picture_obj)
                picture_id = picture_access.get_picture_on_filename(picture_file).id
            user_access.edit_user(current_user.id, first_name, last_name, email, gender, age, phone_number,
                                  user.address, picture_id, send_emails_data)
            flash(lazy_gettext(f'Account edited!'), 'success')
            return redirect(url_for('users.account'))
        elif form.delete.data:
            user = user_access.get_user_on_id(current_user.id)
            address_id = user.address

            # first delete cars bc car has foreign key to user (error if user gets deleted first)
            cars = car_access.get_on_user_id(user.id)
            if cars is not None:
                for car in cars:
                    car_access.delete_car(car.id)

            # then delete user bc user has foreign key to address (error if address gets deleted first)
            user_access.delete_user(user.id)

            # finally delete address, which doesn't have ties to other entries
            if address_id is not None:
                address = address_access.get_on_id(address_id)
                address_access.delete_address(address.id)

            flash(lazy_gettext(f'Account deleted!'), 'success')
            return redirect(url_for('main.home'))

    return render_template('account_edit.html', title=lazy_gettext('Edit account info'), loggedIn=True, form=form)


@users.route("/edit_address", methods=['GET', 'POST'])
def address_edit():
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    form = EditAddressForm()
    if request.method != 'POST':
        user = user_access.get_user_on_id(current_user.id)
        if user.address is None:
            form.street.data = " "
            form.nr.data = " "
            form.city.data = " "
            form.postal_code.data = " "
        else:
            address = address_access.get_on_id(user.address)
            form.street.data = address.street
            form.nr.data = address.nr
            form.city.data = address.city
            form.postal_code.data = address.postal_code
        return render_template('address_edit.html', title=lazy_gettext('Edit address'), loggedIn=True, form=form)

    if form.validate_on_submit():
        street = form.street.data
        nr = str(form.nr.data)
        city = form.city.data
        postal_code = form.postal_code.data

        address_id = None
        user = user_access.get_user_on_id(current_user.id)
        loc = geolocator.geocode(str(street) + " " + str(nr) + " " + str(postal_code) + " " + str(city))
        if loc is None:
            flash(lazy_gettext(f'This address is unknown to us, please check for erros.'), 'danger')
            return render_template('address_edit.html', title=lazy_gettext('Edit address'), loggedIn=True, form=form)
        if user.address is None:
            address_obj = Address(None, "Belgie", city, postal_code, street, nr, None, loc.latitude, loc.longitude)
            address_access.add_address(address_obj)
            address_id = address_access.get_id("Belgie", city, postal_code, street, nr)
        else:
            address = address_access.get_on_id(user.address)
            address_access.edit_address(address.id, street, nr, city, postal_code, "Belgie", loc.latitude, loc.longitude)
            address_id = address.id

        user = user_access.get_user_on_id(current_user.id)
        user_access.edit_user(user.id, user.first_name, user.last_name, user.email, user.gender, user.age,
                              user.phone_number, address_id, user.picture, user.send_emails)
        flash(lazy_gettext(f'Address edited!'), 'success')
        return redirect(url_for('users.account'))
    return render_template('address_edit.html', title=lazy_gettext('Edit address'), loggedIn=True, form=form)

#before/after als datetime, ride.arrival als string?
def filter_rides(rides, before, after):
    print(before, after, rides)
    if before is None and after is None:
        return rides
    else:
        newrides = []
        for ride in rides:
            if before is not None and after is None:
                #TOOO: arrival/departure?
                if ride.arrival_time <= before:
                    newrides.append(ride)
            elif after is not None and before is None:
                #TOOO: arrival/departure?
                if ride.departure_time >= after:
                    newrides.append(ride)
            elif after is not None and before is not None:
                #TOOO: arrival/departure?
                if ride.departure_time >= after and ride.arrival_time <= before:
                    newrides.append(ride)
    return newrides

def get_departure(ride):
    return ride.departure_time

def myrides_help(before, after, shared_with = None):
    before2 = None
    after2 = None
    if before is not None:
        before2 = datetime.strptime(before, "%Y-%m-%d")
    if after is not None:
        after2 = datetime.strptime(after, "%Y-%m-%d")
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    allrides_temp = ride_access.get_on_user_id(current_user.id)
    allrides = filter_rides(allrides_temp,before2,after2)
    if allrides is None:
        allrides = []
    allrides.sort(key=get_departure, reverse=True)
    form = Filter_rides()
    userrides = []
    from_places = []
    to_places = []
    pfps = []
    allids = []
    pickuppoints = []
    pickupbools = []
    for ride in allrides:
        if shared_with is not None:
            if not shared_with in ride_access.find_ride_passengers(ride.id):
                continue
        if ride.user_id == current_user.id:
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
            temp = list(ride_access.get_passenger_ids(ride.id))
            allids.append(temp)
            ride_pfp = []
            #userids = []
            points = []
            bools = [False, False, False]
            for user_id in temp:
                #userids.append(user_id)
                user = user_access.get_user_on_id(user_id)
                if (user.picture) is not None:
                    ride_pfp.append("images/" + str(picture_access.get_picture_on_id(user.picture).filename))
                else:
                    ride_pfp.append("images/temp_profile_pic.png")

            #allids.append(userids)
            pfps.append(ride_pfp)
            if ride.pickup_1 is not None:
                pickup_1 = ride.pickup_1
                time_1 = pickup_1.estimated_time
                points.append(time_1)
                bools[0] = True
                if ride.pickup_2 is not None:
                    pickup_2 = ride.pickup_2
                    time_2 = pickup_2.estimated_time
                    points.append(time_2)
                    bools[1] = True
                    if ride.pickup_3 is not None:
                        pickup_3 = ride.pickup_3
                        time_3 = pickup_3.estimated_time
                        points.append(time_3)
                        bools[2] = True
            pickupbools.append(bools)
            pickuppoints.append(points)

    to_ret = {}
    to_ret["userrides"] = userrides
    to_ret["from_locs"] = from_places
    to_ret["to_locs"] = to_places
    to_ret["pfps"] = pfps
    to_ret["allids"] = allids
    to_ret["pickuppoints"] = pickuppoints
    to_ret["pickupbools"] = pickupbools
    to_ret["form"] = form
    return to_ret

@users.route("/myrides", defaults={'after':None, 'before':None},methods=['GET', 'POST'])
@users.route("/<before>myrides", defaults={'after':None},methods=['GET', 'POST'])
@users.route("/myrides<after>", defaults={'before':None},methods=['GET', 'POST'])
@users.route("/<before>myrides<after>", methods=['GET', 'POST'])
def myrides(before, after):

    form = Filter_rides()
    if form.submit.data:
        if form.before.data and not form.after.data:
            return redirect(url_for('users.myrides', before=str(form.before.data)))
        elif form.after.data and not form.before.data:
            return redirect(url_for('users.myrides', after=str(form.after.data)))
        elif form.after.data and form.before.data:
            before = str(form.before.data)
            after = str(form.after.data)
            return redirect(url_for('users.myrides', before=before, after=after))
        else:
            pass

    res = myrides_help(before, after)

    return render_template('ride_history.html', title=lazy_gettext('My rides'), loggedIn=True, userrides_m=res["userrides"],
                           from_locs_m=res["from_locs"], to_locs_m=res["to_locs"], pfps_m=res["pfps"], allids_m=res["allids"], pickuppoints_m=res["pickuppoints"],
                           pickupbools_m=res["pickupbools"], form=form, before=before, after=after)

def joinedrides_help(before, after, shared_with = None):
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    before2 = None
    after2 = None
    if before is not None:
        before2 = datetime.strptime(before, "%Y-%m-%d")
    if after is not None:
        after2 = datetime.strptime(after, "%Y-%m-%d")
    allrides_temp = ride_access.get_rides_from_passenger(current_user.id)
    allrides = filter_rides(allrides_temp,before2,after2)
    if allrides is None:
        allrides = []
    allrides.sort(key=get_departure, reverse=True)
    form = Filter_rides()
    userrides = []
    from_places = []
    to_places = []
    pfps = []
    allids = []
    pickuppoints = []
    pickupbools = []
    for ride in allrides:
        if shared_with is not None:
            if ride.user_id != shared_with:
                continue
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
        temp = list(ride_access.get_passenger_ids(ride.id))
        temp2 = []
        ride_pfp = []
        userids = []
        points = []
        bools = [False,False,False]

        for user_id in temp:
            if user_id is not current_user.id:
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

    to_ret = {}
    to_ret["userrides"] = userrides
    to_ret["pickuppoints"] = pickuppoints
    to_ret["pickupbools"] = pickupbools
    to_ret["from_locs"] = from_places
    to_ret["to_locs"] = to_places
    to_ret["pfps"] = pfps
    to_ret["form"] = form
    return to_ret

@users.route("/joinedrides", defaults={'after':None, 'before':None},methods=['GET', 'POST'])
@users.route("/<before>joinedrides", defaults={'after':None},methods=['GET', 'POST'])
@users.route("/joinedrides<after>", defaults={'before':None},methods=['GET', 'POST'])
@users.route("/<before>joinedrides<after>", methods=['GET', 'POST'])
def joinedrides(before, after):

    form = Filter_rides()
    if form.submit.data:
        if form.before.data and not form.after.data:
            return redirect(url_for('users.joinedrides', before=str(form.before.data)))
        elif form.after.data and not form.before.data:
            return redirect(url_for('users.joinedrides', after=str(form.after.data)))
        elif form.after.data and form.before.data:
            before = str(form.before.data)
            after = str(form.after.data)
            return redirect(url_for('users.joinedrides', before=before, after=after))
        else:
            pass

    res = joinedrides_help(before, after)

    return render_template('joined_rides.html', title=lazy_gettext('View ride'), loggedIn=True,
                           userrides_j=res["userrides"], pickuppoints_j=res["pickuppoints"], pickupbools_j=res["pickupbools"],
                           from_locs_j=res["from_locs"], to_locs_j=res["to_locs"], pfps_j=res["pfps"], form=form, before=before, after=after)



@users.route("/shared_rides=<userid>")
def shared_rides(userid):
    if not isinstance(userid, int):
        userid = int(userid)
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    j = joinedrides_help(None, None, userid)
    m = myrides_help(None, None, userid)
    target_user = user_access.get_user_on_id(userid)
    if target_user is None:
        abort(404)

    return render_template('shared_rides.html', title=lazy_gettext('Shared rides'), loggedIn=True,
                           userrides_m=m["userrides"],
                           from_locs_m=m["from_locs"], to_locs_m=m["to_locs"], pfps_m=m["pfps"],
                           allids_m=m["allids"], pickuppoints_m=m["pickuppoints"],
                           pickupbools_m=m["pickupbools"], form=m["form"], userrides_j=j["userrides"], pickuppoints_j=j["pickuppoints"], pickupbools_j=j["pickupbools"],
                           from_locs_j=j["from_locs"], to_locs_j=j["to_locs"], pfps_j=j["pfps"], userid=userid, target_user=target_user)


@users.route("/user=<userid>", methods=['GET', 'POST'])
def user(userid):
    if not userid.isdigit():
        abort(404)
    allow_review = False
    if current_user.is_authenticated:
        allow_review = True
    form = Reviews()
    target_user = user_access.get_user_on_id(userid)
    form2 = SelectSubject()

    pfp_path = "images/"
    if target_user.picture is not None:
        pfp_path += picture_access.get_picture_on_id(target_user.picture).filename
    else:
        pfp_path += "temp_profile_pic.png"

    if form2.validate_on_submit() and current_user.is_authenticated:
        user = user_access.get_user_on_id(current_user.id)
        subject = lazy_gettext('Campus Carpool: user message')
        message = lazy_gettext('Dear ') + target_user.first_name + ' ' + target_user.last_name + '\n'
        if form2.subject.data == 'Empty':
            pass
        elif form2.subject.data == 'Lost item':
            subject += lazy_gettext(": Lost item")
            message += lazy_gettext(
                "While carpooling with you recently, I forgot my [ITEM] in your car. Can you let me know if you found it and when you can return it?")
        message += lazy_gettext('\nKind regards\n') + user.first_name + ' ' + user.last_name
        return redirect('mailto:' + target_user.email + '?SUBJECT=' + subject + '&BODY=' + message)
    cars = car_access.get_on_user_id(userid)
    data = review_access.get_on_user_for(userid)
    car_picpaths = []
    if cars == None:
        cars = []
    for car in cars:
        if car.picture is None:
            car_picpaths.append("images/temp_car_pic.jpg")
        else:
            car_picpaths.append("images/" + picture_access.get_picture_on_id(car.picture).filename)
    rev_pfps = []
    mean = 0
    reviews = 0
    for review in data:
        user2 = user_access.get_user_on_id(review.user_from)
        if user2.picture is not None:
            rev_pfps.append("images/" + picture_access.get_picture_on_id(user2.picture).filename)
        else:
            rev_pfps.append("images/temp_profile_pic.png")
        mean += review.amount_of_stars
        reviews += 1
    if reviews > 0:
        mean = mean / reviews

    whole_stars = floor(mean)
    if mean - whole_stars >= 0.3:
        half_stars = 1
    else:
        half_stars = 0

    return render_template('user.html', title=lazy_gettext('User profile'), form=form,
                           target_user=target_user, mean_rate=mean, half_stars=half_stars, whole_stars=whole_stars,
                           data=data, cars=cars, form2=form2, pfp_path=pfp_path, car_picpaths=car_picpaths,
                           allow_review=allow_review, rev_pfps=rev_pfps, userid=userid)  # TODO: same


@users.route("/login", methods=['GET', 'POST'])
def login():
    # makes sure user won`t be able to go to login/register page
    if current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('main.home'))
    form = LoginForm()
    # check if input is valid
    if form.validate_on_submit():
        user = user_access.get_user_on_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.home'))
        else:
            flash(lazy_gettext('Login failed. Please check your email and/or password.'), 'danger')
    return render_template("login.html", title=lazy_gettext("Login"), form=form)


@users.route("/logout")
def logout():
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    logout_user()
    flash(lazy_gettext(f'Succesfully logged out.'), 'success')  # success is for bootstrap class
    return redirect(url_for('main.home'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    # makes sure user won`t be able to go to login/register page
    if current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # check if input is valid

    if form.validate_on_submit():
        user_email = form.email.data
        user_first_name = form.first_name.data
        user_last_name = form.last_name.data
        send_emails = form.send_emails.data
        send_emails_data = 'FALSE'
        if send_emails is True:
            send_emails_data = 'TRUE'
        # decode to make sure it`s a string, not bytes
        user_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_obj = User(first_name=user_first_name, last_name=user_last_name, email=user_email, password=user_password)
        user_obj.send_emails = send_emails_data
        user_access.add_user(user_obj)
        if send_emails is True:
            send_email_signedup(form.email.data)

        fStr1 = lazy_gettext('Account created for')
        fStr2 = lazy_gettext('! You can now log in.')
        flash(f'{fStr1} {form.email.data} {fStr2}', 'success')  # success is for bootstrap class
        return redirect(url_for('users.login'))
    return render_template("register.html", title=lazy_gettext("Register"), form=form)


@users.route("/add_vehicle", methods=['GET', 'POST'])
def add_vehicle():
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    form = VehicleForm()
    if form.validate_on_submit():
        brand = form.brand.data
        model = form.model.data
        color = form.color.data
        plateNumber = form.plateNumber.data
        seats = form.seats.data
        constructionYear = form.constructionYear.data
        consumption = form.consumption.data
        fuelType = form.fuelType.data
        car_obj = Car(None, plateNumber, color, brand, model, seats, constructionYear, consumption, fuelType,
                      current_user.id, None)
        car_access.add_car(car_obj)
        flash(lazy_gettext(f'Vehicle registered!'), 'success')
        return redirect(url_for('users.account'))
    return render_template("add_vehicle.html", title=lazy_gettext("Add Vehicle"), form=form)


@users.route("/edit_vehicle=<car_id>", methods=['GET', 'POST'])
def edit_vehicle(car_id):
    if not car_id.isdigit():
        abort(404)
    if not current_user.is_authenticated and not current_app.config[
        'TESTING']:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
    form = VehicleForm()
    if request.method != 'POST':
        car = car_access.get_on_id(car_id)
        form.brand.data = car.brand
        form.model.data = car.model
        form.color.data = car.color
        form.plateNumber.data = car.number_plate
        form.seats.data = car.nr_seats
        form.constructionYear.data = car.construction_year
        form.consumption.data = car.fuel_consumption
        form.fuelType.data = car.fuel

        return render_template('car_edit.html', title=lazy_gettext('Edit car'), loggedIn=True, form=form, car_id=car_id)

    if form.validate_on_submit():
        brand = form.brand.data
        model = form.model.data
        color = form.color.data
        plateNumber = form.plateNumber.data
        seats = form.seats.data
        constructionYear = form.constructionYear.data
        consumption = form.consumption.data
        fuelType = form.fuelType.data
        picture_id = car_access.get_on_id(car_id).picture

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            picture_obj = Picture(None, filename=picture_file)
            picture_access.add_picture(picture_obj)
            picture_id = picture_access.get_picture_on_filename(picture_file).id

        car_access.edit_car(car_id, brand, model, color, plateNumber, seats, constructionYear, consumption, fuelType,
                            picture_id)
        flash(lazy_gettext(f'Car edited!'), 'success')
        return redirect(url_for('users.account'))
    return render_template('car_edit.html', title=lazy_gettext('Edit car'), loggedIn=True, form=form, car_id=car_id)


@users.route("/delete_vehicle=<car_id>", methods=['GET', 'POST'])
def delete_vehicle(car_id):
    if not car_id.isdigit:
        abort(404)
    # makes sure user won`t be able to go to page without logging in
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))

    car_access.delete_car(car_id)
    flash(lazy_gettext(f'Vehicle deleted!'), 'success')
    return redirect(url_for('users.account'))
