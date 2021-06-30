from .base import DBDocTest


class BaseLoginTest(DBDocTest):
    def setUp(self):
        super(BaseLoginTest, self).setUp()
        self.create_user()


class LoginTest(BaseLoginTest):
    def test_successful(self):
        payload = self.payload({"email": self.email, "password": self.password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(str, type(response.json["token"]))
        self.assertEqual(200, response.status_code)

    def test_incomplete_no_password(self):
        payload = self.payload({"email": self.email})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incomplete_no_email(self):
        payload = self.payload({"password": self.password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incorrect_password(self):
        payload = self.payload({"email": self.email, "password": "cyberpower03"})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.assertEqual(str, type(response.json["error"]))
        self.assertEqual(400, response.status_code)
