from .base import DBDocTest

email = "testman@gmail.com"
password = "cyberpower01"
name = "testy boi"


class SignupTest(DBDocTest):
    def test_successful_signup(self):
        payload = self.payload({"name": name, "email": email, "password": password})
        response = self.app.post(self.routes["signup"], headers=self.json_content, data=payload)
        self.assertEqual(str, type(response.json["id"]))
        self.assertEqual(201, response.status_code)

    def test_incomplete_signup(self):
        payload = self.payload({"email": "testfan@gmail.com", "password": "cyberpower02"})
        response = self.app.post("/auth/signup", headers=self.json_content, data=payload)
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)
