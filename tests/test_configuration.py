from .base import DBDocTest

email = "testman@gmail.com"
password = "cyberpower01"


class BaseConfigurationTest(DBDocTest):
    def setUp(self):
        super(BaseConfigurationTest, self).setUp()
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


class CreateConfigurationTest(BaseConfigurationTest):
    def test_successful(self):
        payload = self.payload({"name": "test_config", "data": {"side": "left", "type": "object"}})
        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, "Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(str, type(response.json["name"]))
        self.assertEqual(dict, type(response.json["data"]))
        self.assertEqual(str, type(response.json["creator"]))
        self.assertEqual(str, type(response.json["_id"]))
        self.assertEqual(201, response.status_code)

    def test_incomplete_no_data(self):
        payload = self.payload({"name": "test_config"})

        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, "Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incomplete_no_name(self):
        payload = self.payload({"data": {"side": "left", "type": "object"}})

        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, "Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)


class GetConfigurationTest(BaseConfigurationTest):
    def setUp(self):
        super(GetConfigurationTest, self).setUp()
        # Create Config
        payload = self.payload({"name": "test_config", "data": {"side": "left", "type": "object"}})
        self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, "Content-Type": "application/json"},
            data=payload,
        )

    def test_successful(self):
        response = self.app.get(
            self.routes["config"] + "/test_config", headers={"Authorization": self.token}
        )
        self.assertEqual(dict, type(response.json["data"]))
        self.assertEqual(str, type(response.json["creator"]))
        self.assertEqual(str, type(response.json["_id"]))
        self.assertEqual(200, response.status_code)

    def test_does_not_exist(self):
        response = self.app.get(
            self.routes["config"] + "/test_config_missing", headers={"Authorization": self.token}
        )
        self.assertEqual(str, type(response.json["error"]))
        self.assertEqual(404, response.status_code)
