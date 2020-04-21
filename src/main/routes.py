from flask import Blueprint, render_template, g, current_app, abort, request, jsonify, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from src.utils import campus_access, user_access, ride_access, address_access
from flask_babel import lazy_gettext
from src.dbmodels.Campus import Campus
from src.dbmodels.Address import Address
from src.dbmodels.Ride import Ride
from flask_login import current_user
from geopy.geocoders import Nominatim
from src.utils import geolocator
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
    return render_template('home.html', users=users, loggedIn=False)


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
    # read json + reply
    data = request.json
    from_coord = data.get('from')
    to_coord = data.get('to')
    time_option = data.get('time_option')
    datetime = data.get('datetime').replace('T', ' ') + ':00'
    print(from_coord, to_coord, time_option, datetime)
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


@main.route('/createRide', methods=['POST'])
def receiver_create():
    # TODO wat met pickup points?
    data = request.json

    # adressen from en to -> campussen of campus en adres
    from_coord = data.get('from')
    to_coord = data.get('to')
    coords = list()
    to_campus = True
    campus_id = 0

    if isinstance(from_coord, int) and not isinstance(to_coord, int):  # p_from is campus, p_to is adres
        campus = campus_access.get_on_id(from_coord)
        campus_id = campus.id
        lat_to = to_coord['lat']
        lng_to = to_coord['lng']
        coords.append(lat_to)
        coords.append(lng_to)
        to_campus = False
    if isinstance(to_coord, int) and not isinstance(from_coord, int):    # p_to is campus, p_from is adres
        campus = campus_access.get_on_id(to_coord)
        campus_id = campus.id
        lat_from = from_coord['lat']
        lng_from = from_coord['lng']
        coords.append(lat_from)
        coords.append(lng_from)
    if isinstance(to_coord, int) and isinstance(from_coord, int):       # p_to and p_from are campussen
        # p_to blijft campus, p_from wordt adres
        campus = campus_access.get_on_id(to_coord)
        campus_id = campus.id

        campus_from = campus_access.get_on_id(from_coord)
        lat_from = campus_from.latitude
        lng_from = campus_from.longitude
        coords.append(lat_from)
        coords.append(lng_from)

    coords_string = "{},{}".format(coords[0], coords[1])
    location = geolocator.reverse(coords_string)
    address = location.raw['address']
    if 'road' in address:
        street = address['road']
    else:
        street = " "
    if 'house_number' in address:
        nr = address['house_number']
    else:
        nr = " "
    if 'postcode' in address:
        postcode = address['postcode']
    else:
        postcode = 0
    if 'town' in address:
        city = address['town']
    else:
        city = " "
    if 'country' in address:
        country = address['country']
    else:
        country = " "

    geo_locatie = street + " " + str(nr) + " " + str(postcode) + " " + city + " " + country
    loc = geolocator.geocode(geo_locatie)
    address_obj = Address(None, country, city, postcode, street, nr, loc.latitude, loc.longitude)
    address_access.add_address(address_obj)
    address_id = address_access.get_id(country, city, postcode, street, nr)

    time_option = data.get('time_option')
    datetime = data.get('datetime').replace('T', ' ') + ':00'

    if time_option == "Arrive by":
        arrival_time = datetime
        departure_time = datetime   # TODO fix
    else:
        departure_time = datetime
        arrival_time = datetime     # TODO fix

    user = user_access.get_user_on_id(current_user.id)
    user_id = user.get_id()

    passengers = data.get('passengers')

    ride = Ride(None, departure_time, arrival_time, user_id, address_id, campus_id, to_campus, None, passengers, None, None, None)
    ride_access.add_ride(ride)
    ride_id = ride_access.get_id_on_all(departure_time, arrival_time, user_id, address_id, campus_id)
    ride_to_return = ride_access.get_on_id(ride_id)

    return jsonify({"ride": ride_to_return.to_dict()})
