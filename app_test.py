import unittest
from src import create_app, TestConfig
from src.utils import user_access, bcrypt
from src.dbmodels.User import User

app = create_app(TestConfig)


def create_test_user():
    """ create a user in the database used for running tests """
    user_password = bcrypt.generate_password_hash('test').decode('utf-8')
    user_obj = User('test', 'test', 'test@blog.com', user_password)
    user_access.add_user(user_obj)


def remove_test_user():
    """ delete the test user from the database """
    user_access.delete_user('test@blog.com')


# source: https://github.com/pallets/flask/blob/master/examples/tutorial/tests/conftest.py
class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


class ProperlyLoaded(FlaskTestCase):
    def test_homepage_properly_loaded(self):
        assert self.client.get("/en/").status_code == 200
        assert self.client.get("/nl/").status_code == 200
        assert self.client.get("/fr/").status_code == 200
        assert self.client.get("/en/home").status_code == 200
        assert self.client.get("/nl/home").status_code == 200
        assert self.client.get("/fr/home").status_code == 200

    def test_about_properly_loaded(self):
        assert self.client.get("/en/about").status_code == 200
        assert self.client.get("/nl/about").status_code == 200
        assert self.client.get("/fr/about").status_code == 200

    def test_faq_properly_loaded(self):
        assert self.client.get("/en/faq").status_code == 200
        assert self.client.get("/nl/faq").status_code == 200
        assert self.client.get("/fr/faq").status_code == 200

    def test_contact_properly_loaded(self):
        assert self.client.get("/en/contact").status_code == 200
        assert self.client.get("/nl/contact").status_code == 200
        assert self.client.get("/fr/contact").status_code == 200

    def test_account_properly_loaded(self):
        assert self.client.get("/en/account").status_code == 200
        assert self.client.get("/nl/account").status_code == 200
        assert self.client.get("/fr/account").status_code == 200

    def test_edit_properly_loaded(self):
        assert self.client.get("/en/edit").status_code == 200
        assert self.client.get("/nl/edit").status_code == 200
        assert self.client.get("/fr/edit").status_code == 200

    def test_myrides_properly_loaded(self):  # TODO: gone??
        assert self.client.get("/en/myrides").status_code == 200
        assert self.client.get("/nl/myrides").status_code == 200
        assert self.client.get("/fr/myrides").status_code == 200

    def test_user_properly_loaded(self):
        assert self.client.get("/en/user=1").status_code == 200
        assert self.client.get("/nl/user=1").status_code == 200
        assert self.client.get("/fr/user=1").status_code == 200

    def test_register_properly_loaded(self):
        assert self.client.get("/en/register").status_code == 200
        assert self.client.get("/nl/register").status_code == 200
        assert self.client.get("/fr/register").status_code == 200

    def test_ride_info_properly_loaded(self):
        assert self.client.get("/en/ride_info").status_code == 200
        assert self.client.get("/nl/ride_info").status_code == 200
        assert self.client.get("/fr/ride_info").status_code == 200

    def test_ride_history_properly_loaded(self):
        assert self.client.get("/en/ride_history").status_code == 200
        assert self.client.get("/nl/ride_history").status_code == 200
        assert self.client.get("/fr/ride_history").status_code == 200

    def test_add_vehicle_properly_loaded(self):
        assert self.client.get("/en/add_vehicle").status_code == 200
        assert self.client.get("/nl/add_vehicle").status_code == 200
        assert self.client.get("/fr/add_vehicle").status_code == 200

    def test_login_properly_loaded(self):
        assert self.client.get("/en/login").status_code == 200
        assert self.client.get("/nl/login").status_code == 200
        assert self.client.get("/fr/login").status_code == 200

    def test_new_review_properly_loaded(self):
        assert self.client.get("/en/user=1/new_review").status_code == 200
        assert self.client.get("/nl/user=1/new_review").status_code == 200
        assert self.client.get("/fr/user=1/new_review").status_code == 200

    def test_findride_properly_loaded(self):
        assert self.client.get("/en/findride").status_code == 200
        assert self.client.get("/nl/findride").status_code == 200
        assert self.client.get("/fr/findride").status_code == 200


if __name__ == '__main__':
    create_test_user()
    unittest.main()
    remove_test_user()
