import json
from nomenclate_api.handlers.documentation import handler
from .base import BaseTest


class DocumentationTest(BaseTest):
    def test_default(self):
        payload = handler(None, None)
        self.assertEqual(payload["statusCode"], 302)
        self.assertEqual(payload["headers"], {"Location": "https://nomenclate.readme.io/"})
        self.assertEqual(payload["body"], json.dumps({}))
