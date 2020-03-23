import os
import tempfile
import unittest
from src import create_app, TestConfig

app = create_app(TestConfig)


# source: https://github.com/pallets/flask/blob/master/examples/tutorial/tests/conftest.py
class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


class ProperlyLoaded(FlaskTestCase):
    def test_homepage_properly_loaded(self):
        assert self.client.get("/").status_code == 200
        assert self.client.get("/home").status_code == 200

    def test_about_properly_loaded(self):
        assert self.client.get("/about").status_code == 200

    def test_faq_properly_loaded(self):
        assert self.client.get("/faq").status_code == 200

    def test_contact_properly_loaded(self):
        assert self.client.get("/contact").status_code == 200

    def test_account_properly_loaded(self):
        assert self.client.get("/account").status_code == 200

    def test_edit_properly_loaded(self):
        assert self.client.get("/edit").status_code == 200

    def test_myrides_properly_loaded(self):
        assert self.client.get("/myrides").status_code == 200

    def test_user_properly_loaded(self):
        assert self.client.get("/user").status_code == 200

    def test_register_properly_loaded(self):
        assert self.client.get("/register").status_code == 200

    def test_ride_info_properly_loaded(self):
        assert self.client.get("/ride_info").status_code == 200

    def test_ride_history_properly_loaded(self):
        assert self.client.get("/ride_history").status_code == 200

    def test_add_vehicle_properly_loaded(self):
        assert self.client.get("/add_vehicle").status_code == 200

    def test_login_properly_loaded(self):
        assert self.client.get("/login").status_code == 200

    def test_newreview_properly_loaded(self):
        assert self.client.get("/newreview").status_code == 200

    def test_findride_properly_loaded(self):
        assert self.client.get("/findride").status_code == 200


if __name__ == '__main__':
    unittest.main()
