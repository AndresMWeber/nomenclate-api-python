import requests
from nomenclate_api import __version__
import nomenclate_api


def test_import():
    assert nomenclate_api


def test_version():
    assert __version__ == "0.1.0"
