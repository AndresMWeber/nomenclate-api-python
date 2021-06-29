from .base import BaseTest
from nomenclate_api.utils.general import get_project_attribute
from nomenclate_api.handlers.version import handler


class VersionTest(BaseTest):
    def test_default(self):
        payload = handler(None, None)
        self.assertEqual(payload["statusCode"], 200)
        self.assertIn(get_project_attribute("tool", "poetry", "version"), payload["body"])
