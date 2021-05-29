import logging
from os import getenv
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("nomenclate-api")
ACCESS_EXPIRES = timedelta(days=7)
REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PASS = getenv("REDIS_PASS", "")
REDIS_PORT = getenv("REDIS_PORT", 6379)
MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017/nomenclate-api")
SESSION_TYPE = "redis"
