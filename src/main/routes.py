from flask import Blueprint, render_template, g, current_app, abort, request, jsonify, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from src.utils import campus_access, user_access, ride_access, address_access, pickup_point_access, car_access
from flask_babel import lazy_gettext
from src.dbmodels.Address import Address
from src.dbmodels.Ride import Ride
from src.dbmodels.PickupPoint import PickupPoint
from flask_login import current_user
from src.users import routes

main = Blueprint('main', __name__, url_prefix='/<lang_code>')


########################################################################################################################
# functions for multilingual support
@main.url_defaults
def add_language_code(endpoint, values):
    if g.lang_code in current_app.config['SUPPORTED_LANGUAGES']:
        values.setdefault('lang_code', g.lang_code)
    else:
        values.setdefault('lang_code', 'en')


@main.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@main.before_request
def before_request():
    if g.lang_code not in current_app.config['SUPPORTED_LANGUAGES']:
        abort(404)


########################################################################################################################


@main.route("/")
@main.route("/home")
def home():
    users = user_access.get_users()
    interested = True
    if current_user.is_authenticated:
        interested = False
    return render_template('home.html', users=users, loggedIn=False, displayinterested=interested)


@main.route("/about")
def about():
    return render_template('about.html', title=lazy_gettext('About'), loggedIn=False)


@main.route("/faq")
def faq():
    return render_template('faq.html', title=lazy_gettext('FAQ'), loggedIn=False)


@main.route("/contact")
def contact():
    return render_template('contact.html', title=lazy_gettext('contact'), loggedIn=False)


@main.route('/calculateCompatibleRides', methods=['POST'])
def receiver():
    from time import time
    start = time()
    # read json + reply
    data = request.json
    from_coord = data.get('from')
    to_coord = data.get('to')
    time_option = data.get('time_option')
    datetime = data.get('datetime').replace('T', ' ') + ':00'
    rides = ride_access.match_rides_with_passenger(from_coord, to_coord, time_option, datetime)
    results = []
    drivers = []
    for ride in rides:
        results.append(ride.to_dict())
        driver_id = ride.user_id
        driver = user_access.get_user_on_id(driver_id)
        drivers.append(driver.to_dict())
    return jsonify({"results": results, "drivers": drivers})


@main.route('/fillschools', methods=['POST'])
def get_schools():
    schools = dict()

    campus_objects = campus_access.get_all()
    for campus in campus_objects:
        schools[campus.id] = campus.to_dict()
    return schools


@main.route('/canceljoinedride=<ride_id>', methods=['POST', 'GET'])
def canceljoinedride(ride_id):
    if not current_user.is_authenticated and not current_app.config[
        'TESTING']:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))

    ride_access.delete_passenger(current_user.id, ride_id)
    flash('Canceled ride.', 'success')
    return redirect(url_for('users.account'))


@main.route('/deleteride=<ride_id>', methods=['POST', 'GET'])
def deleteride(ride_id):
    if not current_user.is_authenticated and not current_app.config[
        'TESTING']:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))

    ride_access.delete_from_passenger_ride(ride_id)
    ride_access.delete_ride(ride_id)
    flash('Deleted ride.', 'success')
    return redirect(url_for('users.account'))


@main.route('/createRide', methods=['POST'])
def receiver_create():
    data = request.json
    # adressen from en to -> campussen of campus en adress
    from_coord = data.get('from')
    to_coord = data.get('to')
    coords = list()

    if isinstance(from_coord, int):
        campus_from = from_coord
        address_from = None
    else:
        campus_from = None
        lat_from = from_coord['lat']
        lng_from = from_coord['lng']
        coords.append(lat_from)
        coords.append(lng_from)
        address_from = Address(None, None, None, None, None, None, None, lat_from, lng_from)
        address_access.add_address(address_from)
        address_from = address_from.fetch_id()
    if isinstance(to_coord, int):
        campus_to = to_coord
        address_to = None
    else:
        campus_to = None
        lat_to = to_coord['lat']
        lng_to = to_coord['lng']
        coords.append(lat_to)
        coords.append(lng_to)
        address_to = Address(None, None, None, None, None, None, None, lat_to, lng_to)
        address_access.add_address(address_to)
        address_to = address_to.fetch_id()

    time_option = data.get('time_option')
    datetime = data.get('datetime')
    arrival_time = data.get('arrive_time')
    departure_time = data.get('depart_time')

    user = user_access.get_user_on_id(current_user.id)
    user_id = user.get_id()

    passengers = data.get('passengers')
    pickup_points = data.get('pickup_points')   # tuples van coordinaten
    pick_up_ids = list()
    estimated_times = data.get('estimated_times')
    index = 0
    for point in pickup_points:
        latitude = point['lat']
        longitude = point['lng']
        estimated_time = estimated_times[index]
        point = PickupPoint(None, estimated_time, latitude, longitude)
        pickup_point_access.add_pickup_point(point)
        point_id = pickup_point_access.get_id(latitude, longitude)
        pick_up_ids.append(point_id)
        index += 1

    cars = car_access.get_on_user_id(user.id)
    if len(cars) == 0:
        car = None
    else:
        car = cars[0]

    ride = None
    if len(pick_up_ids) == 0:
        ride = Ride(None, departure_time, arrival_time, user_id, car.id, passengers, None, None, None, campus_from,
                    campus_to, address_from, address_to)
    if len(pick_up_ids) == 1:
        ride = Ride(None, departure_time, arrival_time, user_id, car.id, passengers, pick_up_ids[0], None, None,
                    campus_from, campus_to, address_from, address_to)
    if len(pick_up_ids) == 2:
        ride = Ride(None, departure_time, arrival_time, user_id, car.id, passengers, pick_up_ids[0], pick_up_ids[1],
                    None, campus_from, campus_to, address_from, address_to)
    if len(pick_up_ids) == 3:
        ride = Ride(None, departure_time, arrival_time, user_id, car.id, passengers, pick_up_ids[0], pick_up_ids[1],
                    pick_up_ids[2], campus_from, campus_to, address_from, address_to)

    ride_access.add_ride(ride)
    ride_id = ride_access.get_id_on_all(departure_time, arrival_time, user_id, ride.address_from, ride.address_to)
    ride_to_return = ride_access.get_on_id(ride_id)

    return jsonify({"ride": ride_to_return.to_dict()})
