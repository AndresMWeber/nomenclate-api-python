from .base import DBDocTest

email = "testman@gmail.com"
password = "cyberpower01"


class LoginTest(DBDocTest):
    def setUp(self):
        super(LoginTest, self).setUp()
        payload = self.payload({"name": "testy boi", "email": email, "password": password})
        self.app.post(self.routes["signup"], headers=self.json_content, data=payload)

    def test_successful(self):
        payload = self.payload({"email": email, "password": password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(str, type(response.json["token"]))
        self.assertEqual(200, response.status_code)

    def test_incomplete_no_password(self):
        payload = self.payload({"email": email})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incomplete_no_email(self):
        payload = self.payload({"password": password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incorrect_password(self):
        payload = self.payload({"email": email, "password": "cyberpower03"})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(str, type(response.json["error"]))
        self.assertEqual(400, response.status_code)
