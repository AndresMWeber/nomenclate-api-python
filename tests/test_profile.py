from .base import DBDocTest


class ProfileTest(DBDocTest):
    def setUp(self):
        super(ProfileTest, self).setUp()
        self.create_user()
        self.log_in_user()

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
