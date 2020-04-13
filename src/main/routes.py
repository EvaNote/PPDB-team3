from flask import Blueprint, render_template, g, current_app, abort, request
from flask_login import current_user
from flask_babel import lazy_gettext
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
    users = None  # user_access.get_users()
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

    result = "start: {}, {} — end: {}, {}".format(data['from']['lat'], data['from']['lng'],
                                                  data['to']['lat'], data['to']['lng'])
    return result


@main.route('/fillschools', methods=['POST'])
def get_schools():
    schools = dict()
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    locations = geolocator.geocode('Universiteit België', False, limit=100000, timeout=30)
    for location in locations:
        location.raw['soort'] = 'u'
        schools[location.raw['osm_id']] = location.raw
        print(location.raw)
    locations = geolocator.geocode('Hogeschool België', False, limit=100000, timeout=30)
    for location in locations:
        schools[location.raw['osm_id']] = location.raw
        location.raw['soort'] = 'h'
        print(location.raw)
    return schools
