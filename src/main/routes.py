from flask import Blueprint, render_template, g, current_app, abort, request, jsonify
from src.utils import campus_access, user_access, ride_access
from flask_babel import lazy_gettext
from src.dbmodels.Campus import Campus
from flask_login import current_user
from geopy.geocoders import Nominatim

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
    # read json + reply
    data = request.json
    from_coord = data.get('from')
    to_coord = data.get('to')
    time_option = data.get('time_option')
    datetime = data.get('datetime').replace('T', ' ') + ':00'
    #rides = ride_access.match_rides_with_passenger(from_coord, to_coord, time_option, datetime)
    results = []
    #for ride in rides:
    #    results.append(ride.to_dict())
    return jsonify({"results": results})


@main.route('/fillschools', methods=['POST'])
def get_schools():
    schools = dict()

    campus_objects = campus_access.get_all()
    for campus in campus_objects:
        schools[campus.id] = campus.to_dict()

    # geolocator = Nominatim(user_agent="specify_your_app_name_here")
    # locations = geolocator.geocode('Universiteit België', False, limit=100000, timeout=30)
    # for location in locations:
    #     location.raw['soort'] = 'u'
    #     schools[location.raw['osm_id']] = location.raw
    #     print(location.raw)
    # locations = geolocator.geocode('Hogeschool België', False, limit=100000, timeout=30)
    # for location in locations:
    #     schools[location.raw['osm_id']] = location.raw
    #     location.raw['soort'] = 'h'
    #     print(location.raw)
    return schools
