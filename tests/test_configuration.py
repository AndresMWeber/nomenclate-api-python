from .base import DBDocTest


class BaseConfigurationTest(DBDocTest):
    def setUp(self):
        super(BaseConfigurationTest, self).setUp()
        self.create_user()
        self.log_in_user()


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
        self.create_config()

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
        self.create_config()
        response = self.app.delete(
            f'{self.routes["config"]}/{self.config["name"]}', headers={"Authorization": self.token}
        )
        self.assertEqual(200, response.status_code)
