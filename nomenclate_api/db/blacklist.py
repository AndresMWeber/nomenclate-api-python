from redis import StrictRedis
from nomenclate_api.config import ACCESS_EXPIRES, LOG, REDIS_HOST, REDIS_PASS, REDIS_PORT

jwt_redis_blocklist = None
try:
    jwt_redis_blocklist = StrictRedis(
        host=REDIS_HOST, password=REDIS_PASS, port=REDIS_PORT, db=0, decode_responses=True
    )
except:
    LOG.log_error("Could not connect to redis.")


def blacklist_token(token):
    try:
        jwt_redis_blocklist.set(token, "", ex=ACCESS_EXPIRES)
    except Exception as e:
        LOG.warning(e)


def init_blacklist(app, jwt):
    jwt._set_error_handler_callbacks(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        if jwt_redis_blocklist:
            jti = jwt_payload["jti"]
            token_in_redis = jwt_redis_blocklist.get(jti)
            return token_in_redis is not None
        return True
