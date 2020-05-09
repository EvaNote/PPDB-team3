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
        # need at least one user for some of the tests below, so make sure there is at least one
        # user_email = 'test@blog.com'
        # user_first_name = 'test'
        # user_last_name = 'test'
        # from src.utils import user_access, bcrypt
        # user_password = bcrypt.generate_password_hash('test').decode('utf-8')
        # self.user_obj = User(first_name=user_first_name, last_name=user_last_name, email=user_email,
        #                      password=user_password)
        # user_access.add_user(self.user_obj)

    def tearDown(self):
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def check_status_code_three_languages(self, url):
        assert self.client.get("/en" + url).status_code == 200
        assert self.client.get("/fr" + url).status_code == 200
        assert self.client.get("/nl" + url).status_code == 200


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
    # new review: '/user=<userid>/new_review' TODO
    ...


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

    # user profile: '/user=<userid>' TODO

    # login: '/login'
    def test_login_properly_loaded(self):
        self.check_status_code_three_languages('/login')

    # logout: '/logout' TODO

    # signup: '/register'
    def test_register_properly_loaded(self):
        self.check_status_code_three_languages('/register')

    # add car: '/add_vehicle'
    def test_add_vehicle_properly_loaded(self):
        self.check_status_code_three_languages('/add_vehicle')

    # edit car: '/edit_vehicle=<car_id>' TODO

    # delete car: '/delete_vehicle=<car_id>' TODO


# class ProperlyLoaded(FlaskTestCase):
#     def test_homepage_properly_loaded(self):
#         assert self.client.get("/en/").status_code == 200
#         assert self.client.get("/nl/").status_code == 200
#         assert self.client.get("/fr/").status_code == 200
#         assert self.client.get("/en/home").status_code == 200
#         assert self.client.get("/nl/home").status_code == 200
#         assert self.client.get("/fr/home").status_code == 200
#
#     def test_about_properly_loaded(self):
#         assert self.client.get("/en/about").status_code == 200
#         assert self.client.get("/nl/about").status_code == 200
#         assert self.client.get("/fr/about").status_code == 200
#
#     def test_faq_properly_loaded(self):
#         assert self.client.get("/en/faq").status_code == 200
#         assert self.client.get("/nl/faq").status_code == 200
#         assert self.client.get("/fr/faq").status_code == 200
#
#     def test_contact_properly_loaded(self):
#         assert self.client.get("/en/contact").status_code == 200
#         assert self.client.get("/nl/contact").status_code == 200
#         assert self.client.get("/fr/contact").status_code == 200
#
#     def test_account_properly_loaded(self):
#         assert self.client.get("/en/account").status_code == 200
#         assert self.client.get("/nl/account").status_code == 200
#         assert self.client.get("/fr/account").status_code == 200
#
#     def test_edit_properly_loaded(self):
#         assert self.client.get("/en/edit").status_code == 200
#         assert self.client.get("/nl/edit").status_code == 200
#         assert self.client.get("/fr/edit").status_code == 200
#
#     def test_myrides_properly_loaded(self):  # TODO: gone??
#         assert self.client.get("/en/myrides").status_code == 200
#         assert self.client.get("/nl/myrides").status_code == 200
#         assert self.client.get("/fr/myrides").status_code == 200
#
#     def test_user_properly_loaded(self):
#         assert self.client.get("/en/user=1").status_code == 200
#         assert self.client.get("/nl/user=1").status_code == 200
#         assert self.client.get("/fr/user=1").status_code == 200
#
#     def test_register_properly_loaded(self):
#         assert self.client.get("/en/register").status_code == 200
#         assert self.client.get("/nl/register").status_code == 200
#         assert self.client.get("/fr/register").status_code == 200
#
#     def test_ride_info_properly_loaded(self):
#         assert self.client.get("/en/ride_info").status_code == 200
#         assert self.client.get("/nl/ride_info").status_code == 200
#         assert self.client.get("/fr/ride_info").status_code == 200
#
#     def test_ride_history_properly_loaded(self):
#         assert self.client.get("/en/ride_history").status_code == 200
#         assert self.client.get("/nl/ride_history").status_code == 200
#         assert self.client.get("/fr/ride_history").status_code == 200
#
#     def test_add_vehicle_properly_loaded(self):
#         assert self.client.get("/en/add_vehicle").status_code == 200
#         assert self.client.get("/nl/add_vehicle").status_code == 200
#         assert self.client.get("/fr/add_vehicle").status_code == 200
#
#     def test_login_properly_loaded(self):
#         assert self.client.get("/en/login").status_code == 200
#         assert self.client.get("/nl/login").status_code == 200
#         assert self.client.get("/fr/login").status_code == 200
#
#     def test_new_review_properly_loaded(self):
#         assert self.client.get("/en/user=1/new_review").status_code == 200
#         assert self.client.get("/nl/user=1/new_review").status_code == 200
#         assert self.client.get("/fr/user=1/new_review").status_code == 200
#
#     def test_findride_properly_loaded(self):
#         assert self.client.get("/en/findride").status_code == 200
#         assert self.client.get("/nl/findride").status_code == 200
#         assert self.client.get("/fr/findride").status_code == 200


if __name__ == '__main__':
    unittest.main()
