from os import getenv
from datetime import timedelta
from logging import getLogger

LOG = getLogger()
ACCESS_EXPIRES = timedelta(days=7)
REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PASS = getenv("REDIS_PASS", "")
REDIS_PORT = getenv("REDIS_PORT", 6379)
MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017/nomenclate-api")
