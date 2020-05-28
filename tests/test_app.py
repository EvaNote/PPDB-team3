import os
import sys
cwd = os.getcwd()
sys.path.append(cwd[0:len(cwd)-6])
import tempfile
import unittest
from src import create_app, TestConfig
from flask_login import current_user, login_user, logout_user
from src.dbmodels.User import User
import base64

app = create_app(TestConfig)


@app.route('/test_login')
def test_login():
    from src.utils import user_access
    user = user_access.get_user_on_email('lui@campuscarpool.com')
    print(user)
    result = login_user(user, remember=True)
    print(result)
    return 'something'


# source: https://github.com/pallets/flask/blob/master/examples/tutorial/tests/conftest.py
class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.client.get('/test_login')
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def check_status_code_three_languages(self, url, expected_status_code=200):
        print(self.client.get("/en" + url).status_code)
        assert self.client.get("/en" + url).status_code == expected_status_code
        assert self.client.get("/fr" + url).status_code == expected_status_code
        assert self.client.get("/nl" + url).status_code == expected_status_code


class ProperlyLoadedMainGetRoutes(FlaskTestCase):
    # home: '/' and '/home'
    def test_home_properly_loaded(self):
        self.check_status_code_three_languages('/')
        self.check_status_code_three_languages('/home')

    # about: '/about'
    def test_about_properly_loaded(self):
        self.check_status_code_three_languages('/about')

    # faq: '/faq'
    def test_faq_properly_loaded(self):
        self.check_status_code_three_languages('/faq')

    # contact: '/contact'
    def test_contact_properly_loaded(self):
        self.check_status_code_three_languages('/contact')


class ProperlyLoadedReviewsGetRoutes(FlaskTestCase):
    # new review: '/user=<userid>/new_review'
    def test_new_review_properly_loaded(self):
        self.check_status_code_three_languages('/user=1/new_review')


class ProperlyLoadedRidesGetRoutes(FlaskTestCase):
    # find ride: '/findride'
    def test_find_ride_properly_loaded(self):
        self.check_status_code_three_languages('/findride')

    # create ride: '/createride'
    def test_create_ride_properly_loaded(self):
        self.check_status_code_three_languages('/createride')

    # ride info: '/ride_info'
    def test_ride_info_properly_loaded(self):
        self.check_status_code_three_languages('/ride_info')

    # ride history: "/ride_history'
    def test_ride_history_properly_loaded(self):
        self.check_status_code_three_languages('/ride_history')


class ProperlyLoadedUsersGetRoutes(FlaskTestCase):
    # account: '/account'
    def test_account_properly_loaded(self):
        self.check_status_code_three_languages('/account')

    # account edit: '/edit'
    def test_edit_properly_loaded(self):
        self.check_status_code_three_languages('/edit')

    # address edit: '/edit_address'
    def test_edit_address_properly_loaded(self):
        self.check_status_code_three_languages('/edit_address')

    # my rides: '/myrides'
    def test_my_rides_properly_loaded(self):
        self.check_status_code_three_languages('/myrides')

    # joined rides: '/joinedrides'
    def test_joined_rides_properly_loaded(self):
        self.check_status_code_three_languages('/joinedrides')

    # user profile: '/user=<userid>'
    def test_user_profile_properly_loaded(self):
        self.check_status_code_three_languages('/user=1')

    # login: '/login'
    def test_login_properly_loaded(self):
        self.check_status_code_three_languages('/login')

    # logout: '/logout'
    def test_logout_properly_loaded(self):
        self.check_status_code_three_languages('/logout', 302)  # found, redirect

    # signup: '/register'
    def test_register_properly_loaded(self):
        self.check_status_code_three_languages('/register')

    # add car: '/add_vehicle'
    def test_add_vehicle_properly_loaded(self):
        self.check_status_code_three_languages('/add_vehicle')

    # edit car: '/edit_vehicle=<car_id>'
    def test_edit_vehicle_properly_loaded(self):
        self.check_status_code_three_languages('/edit_vehicle=1')

    # delete car: '/delete_vehicle=<car_id>'
    def test_delete_vehicle_properly_loaded(self):
        self.check_status_code_three_languages('/delete_vehicle=2', 302)  # found, redirect


if __name__ == '__main__':
    unittest.main()
