from .test_configuration import BaseConfigurationTest


class BaseNomenclateTest(BaseConfigurationTest):
    def setUp(self):
        super(BaseNomenclateTest, self).setUp()
        self.create_config()
        self.set_active_config()


class CreateNomenclateTest(BaseNomenclateTest):
    def test_successful(self):
        payload = self.payload({"name": "test_nom", "data": {"side": "left", "type": "object"}})
        response = self.app.post(
            self.routes["nomenclate"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        nomenclate = response.json["nomenclate"]
        self.assertEqual(str, type(nomenclate["name"]))
        self.assertEqual(dict, type(nomenclate["data"]))
        self.assertEqual(str, type(nomenclate["creator"]))
        self.assertEqual(str, type(nomenclate["_id"]))
        self.assertEqual(201, response.status_code)

    def test_incomplete_no_data(self):
        payload = self.payload({"name": "test_nom"})

        response = self.app.post(
            self.routes["nomenclate"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)

    def test_incomplete_no_name(self):
        payload = self.payload({"data": {"side": "left", "type": "object"}})

        response = self.app.post(
            self.routes["nomenclate"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.assertEqual(dict, type(response.json["error"]))
        self.assertEqual(400, response.status_code)


class GetNomenclateTest(BaseNomenclateTest):
    nomenclate_data = {"side": "right", "type": "locator"}

    def setUp(self):
        super(GetNomenclateTest, self).setUp()
        self.config = self.create_nomenclate(data=self.nomenclate_data.copy())

    def test_successful(self):
        response = self.app.get(
            f"{self.routes['nomenclate']}/{self.nomenclate['_id']}",
            headers={"Authorization": self.token},
        )
        self.assertEqual(dict, type(response.json["data"]))
        self.assertEqual(str, type(response.json["creator"]))
        self.assertEqual(str, type(response.json["_id"]))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.nomenclate_data, response.json["data"])

    def test_does_not_exist(self):
        response = self.app.get(
            f"{self.routes['nomenclate']}/1234",
            headers={"Authorization": self.token},
        )
        self.assertEqual(str, type(response.json["error"]))
        self.assertEqual(404, response.status_code)


class PutNomenclateTest(BaseNomenclateTest):
    def test_successful_put(self):
        payload = self.payload(
            {
                **self.create_nomenclate(),
                **{
                    "name": "test_nomenclate_put",
                    "data": {"suffix": "post", "side": "center", "type": "polgyon"},
                },
            },
        )
        response = self.app.put(
            f"{self.routes['nomenclate']}",
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.assertEqual(204, response.status_code)


class DeleteNomenclateTest(BaseNomenclateTest):
    def test_successful_delete(self):
        nom = self.create_nomenclate()
        response = self.app.delete(
            f'{self.routes["nomenclate"]}/{nom["_id"]}', headers={"Authorization": self.token}
        )
        self.assertEqual(200, response.status_code)
