import json
from .base import DBDocTest

email = "testman@gmail.com"
password = "cyberpower01"


class ProfileTest(DBDocTest):
    def setUp(self):
        super(ProfileTest, self).setUp()
        # Create user
        payload = self.payload({"name": "testy boi", "email": email, "password": password})
        self.app.post(self.routes["signup"], headers=self.json_content, data=payload)

        # Log in user
        payload = self.payload({"email": email, "password": password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.token = f'Bearer {response.json["token"]}'

    def test_already_active(self):
        payload = self.payload({"email": email, "password": password})
        response = self.app.post(self.routes["reactivate"], headers=self.json_content, data=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json["message"]))

    def test_successful_deactivate_then_activate(self):
        payload = self.payload({"email": email, "password": password})
        response = self.app.post(self.routes["deactivate"], headers={"Authorization": self.token})
        self.assertEqual(200, response.status_code)

        self.assertEqual(bool, type(response.json["success"]))

        response = self.app.post(self.routes["reactivate"], headers=self.json_content, data=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual(bool, type(response.json["success"]))
