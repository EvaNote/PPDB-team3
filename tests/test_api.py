import os
import sys
cwd = os.getcwd()
sys.path.append(cwd[0:len(cwd)-6])
import tempfile
import unittest
from src import create_app, TestConfig
from src.dbmodels.User import User

app = create_app(TestConfig)


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.test_user = {"username": "test", "firstname": "test", "lastname": "test", "password": "test_password"}

    def tearDown(self):
        from src.utils import user_access, bcrypt
        user = user_access.get_user_on_email(self.test_user.get("username") + "@campuscarpool.com")
        user_access.delete_user(user.id)

    def test_users_1_register_status_code(self):
        r = self.client.post("/api/users/register", json=self.test_user)
        assert r.status_code == 201
        assert r.headers["Content-Type"] == "application/json"
        assert "id" in r.json
        r = self.client.post("/api/users/register", json=self.test_user)
        assert r.status_code == 400
        assert r.headers["Content-Type"] == "application/json"
        assert "message" in r.json  # there is an error message in the body

    def test_users_2_auth_status_code(self):
        from src.utils import user_access, bcrypt
        user_access.add_user(User(self.test_user.get("firstname"), self.test_user.get("lastname"),
                                  self.test_user.get("username") + "@campuscarpool.com",
                                  bcrypt.generate_password_hash(self.test_user.get("password")).decode("utf-8")))
        r = self.client.post("/api/users/auth", json={"username": self.test_user.get("username"),
                                                      "password": self.test_user.get("password")})
        assert r.status_code == 200
        assert r.headers["Content-Type"] == "application/json"
        assert "token" in r.json
        r = self.client.post("/api/users/auth", json={"username": self.test_user["username"],
                                                      "password": "invalid_password"})
        assert r.status_code == 401
        assert r.headers["Content-Type"] == "application/json"
        assert "message" in r.json


if __name__ == '__main__':
    unittest.main()
