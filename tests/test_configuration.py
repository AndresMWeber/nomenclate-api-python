import random
from .base import DBDocTest

email = "testman@gmail.com"
password = "cyberpower01"


class BaseConfigurationTest(DBDocTest):
    config = None

    def create_config(self):
        payload = self.payload(
            {
                "name": f"test_config{hash(random.getrandbits(128))}",
                "data": {"side": "left", "type": "object"},
            }
        )
        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        return response.json

    def setUp(self):
        super(BaseConfigurationTest, self).setUp()
        # Create user
        payload = self.payload({"name": "testy boi", "email": email, "password": password})
        self.app.post(self.routes["signup"], headers=self.json_content, data=payload)

        # Log in user
        payload = self.payload({"email": email, "password": password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.token = f'Bearer {response.json["token"]}'


class CreateConfigurationTest(BaseConfigurationTest):
    def test_successful(self):
        payload = self.payload({"name": "test_config", "data": {"side": "left", "type": "object"}})
        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, **self.json_content},
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
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incomplete_no_name(self):
        payload = self.payload({"data": {"side": "left", "type": "object"}})

        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)


class GetConfigurationTest(BaseConfigurationTest):
    def setUp(self):
        super(GetConfigurationTest, self).setUp()
        # Create Config
        self.config = self.create_config()

    def test_successful(self):
        response = self.app.get(
            f"{self.routes['config']}/{self.config['name']}", headers={"Authorization": self.token}
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


class PutConfigurationTest(BaseConfigurationTest):
    def test_successful_put(self):
        payload = self.payload(
            {
                **self.create_config(),
                **{
                    "name": "test_config_put",
                    "data": {"suffix": "post", "side": "right", "type": "object"},
                },
            },
        )
        response = self.app.put(
            self.routes["config"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.assertEqual(204, response.status_code)


class DeleteConfigurationTest(BaseConfigurationTest):
    def test_successful_delete(self):
        config = self.create_config()
        response = self.app.delete(
            f'{self.routes["config"]}/{config["name"]}', headers={"Authorization": self.token}
        )
        self.assertEqual(200, response.status_code)
