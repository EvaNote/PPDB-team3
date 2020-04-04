import unittest
from src import create_app, TestConfig
from src.utils import user_access, bcrypt
from src.dbmodels.User import User

app = create_app(TestConfig)


class APITestCase(unittest.TestCase):
    test_user = {"username": "test", "firstname": "test", "lastname": "test", "password": "test_password"}

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def tearDown(self):
        user_access.delete_user(self.test_user.get("username") + "@campuscarpool.com")

    def test_users_register_status_code(self):
        r = self.client.post("/api/users/register", json=self.test_user)
        assert r.status_code == 201
        assert r.headers["Content-Type"] == "application/json"
        assert "id" in r.json
        r = self.client.post("/api/users/register", json=self.test_user)
        assert r.status_code == 400
        assert r.headers["Content-Type"] == "application/json"
        assert "message" in r.json  # there is an error message in the body

    def test_users_auth_status_code(self):
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
