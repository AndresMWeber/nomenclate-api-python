import json
from .base import DBDocTest

email = "testman@gmail.com"
password = "cyberpower01"


class ProfileTest(DBDocTest):
    def setUp(self):
        super(ProfileTest, self).setUp()
        # Create user
        payload = self.payload({"name": "testy boi", "email": email, "password": password})
        self.app.post(
            self.routes["signup"], headers={"Content-Type": "application/json"}, data=payload
        )

        # Log in user
        payload = self.payload({"email": email, "password": password})
        response = self.app.post(
            self.routes["login"], headers={"Content-Type": "application/json"}, data=payload
        )
        self.token = f'Bearer {response.json["token"]}'

    def test_successful(self):
        response = self.app.get(self.routes["profile"], headers={"Authorization": self.token})
        self.assertEqual(str, type(response.json["_id"]))
        self.assertEqual(bool, type(response.json["active"]))
        self.assertEqual(str, type(response.json["email"]))
        self.assertEqual(str, type(response.json["name"]))
        self.assertEqual(200, response.status_code)

    def test_successful_active_config(self):
        response = self.app.get(
            self.routes["profile_active_config"], headers={"Authorization": self.token}
        )
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json["configuration"])

    def test_successful_configs(self):
        response = self.app.get(
            self.routes["profile_configs"], headers={"Authorization": self.token}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json["configurations"]))
