from .test_nomenclate import BaseNomenclateTest


class BaseFormattedTest(BaseNomenclateTest):
    def setUp(self):
        super(BaseFormattedTest, self).setUp()
        self.create_nomenclate()


class GetFormattedTest(BaseFormattedTest):
    def test_successful(self):
        self.create_nomenclate({"side": "left", "type": "locator", "name": "john"})
        id = self.nomenclate.get("_id")
        response = self.app.get(
            f"{self.routes['formatted']}/{id}",
            headers={"Authorization": self.token},
        )
        self.assertEqual(str, type(response.json["data"]))
        self.assertEqual("john_l_LOC", response.json["data"])
        self.assertEqual(200, response.status_code)

    def test_does_not_exist(self):
        response = self.app.get(
            self.routes["formatted"] + "/test_nomenclate_missing",
            headers={"Authorization": self.token},
        )
        self.assertEqual(str, type(response.json["error"]))
        self.assertEqual(404, response.status_code)
