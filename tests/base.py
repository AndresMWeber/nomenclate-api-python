import os
import json
import unittest
from nomenclate_api.api import app
from nomenclate_api.db.mongo import db


class BaseTest(unittest.TestCase):
    pass


class DBDocTest(BaseTest):
    json_content = {"Content-Type": "application/json"}
    routes = {
        "login": "/auth/login",
        "signup": "/auth/signup",
        "reactivate": "/auth/reactivate",
        "deactivate": "/auth/deactivate",
        "config": "/config",
        "profile": "/me",
        "profile_configs": "/me/configs",
        "profile_active_config": "/me/config",
        "nomenclate": "/nomenclate",
    }

    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def tearDown(self):
        with app.app_context():
            self.db.connection.drop_database("nomenclate-api")

    def payload(self, payload):
        return json.dumps(payload)
