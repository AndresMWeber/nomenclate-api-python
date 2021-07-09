import random
import json
import unittest
from nomenclate_api.api import app
from nomenclate_api.db.mongo import db
from .sample_config import sample_config


class BaseTest(unittest.TestCase):
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
        "formatted": "/format",
    }
    email = "testman@gmail.com"
    password = "cyberpower01"
    name = "testy boi"
    config = None
    token = None
    nomenclate = None

    def create_user(self):
        payload = self.payload({"name": self.name, "email": self.email, "password": self.password})
        self.app.post(self.routes["signup"], headers=self.json_content, data=payload)

    def log_in_user(self):
        payload = self.payload({"email": self.email, "password": self.password})
        response = self.app.post(self.routes["login"], headers=self.json_content, data=payload)
        self.token = f'Bearer {response.json["token"]}'

    def create_config(self, data={"side": "left", "type": "object"}):
        payload = self.payload(
            {
                "name": f"test_config{hash(random.getrandbits(128))}",
                "data": data,
            }
        )
        response = self.app.post(
            self.routes["config"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.config = response.json
        return self.config

    def set_active_config(self, name=None):
        payload = self.payload({"name": name or self.config["name"]})
        self.app.post(
            self.routes["profile_active_config"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )

    def create_nomenclate(self, data={"side": "left", "type": "object"}):
        self.create_config(sample_config)
        self.set_active_config()
        payload = self.payload(
            {
                "name": f"test_nom{hash(random.getrandbits(128))}",
                "data": data,
                "format_string": "name_side_type",
            }
        )
        response = self.app.post(
            self.routes["nomenclate"],
            headers={"Authorization": self.token, **self.json_content},
            data=payload,
        )
        self.nomenclate = response.json["nomenclate"]
        return self.nomenclate


class DBDocTest(BaseTest):
    json_content = {"Content-Type": "application/json"}

    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def tearDown(self):
        with app.app_context():
            self.db.connection.drop_database("nomenclate-api")

    def payload(self, payload):
        return json.dumps(payload)
