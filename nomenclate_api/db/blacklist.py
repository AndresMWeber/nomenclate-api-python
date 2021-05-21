from redis import StrictRedis
from nomenclate_api.config import ACCESS_EXPIRES, LOG, REDIS_HOST, REDIS_PASS, REDIS_PORT

jwt_redis_blacklist = None


def blacklist_token(token):
    try:
        jwt_redis_blacklist.set(token, "", ex=ACCESS_EXPIRES)
    except Exception as e:
        LOG.warning(e)


def init_blacklist(app, jwt):
    try:
        jwt_redis_blacklist = StrictRedis(
            host=REDIS_HOST, password=REDIS_PASS, port=REDIS_PORT, db=0, decode_responses=True
        )
    except:
        LOG.log_error("Could not connect to redis.")

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        try:
            jti = jwt_payload["jti"]
            token_in_redis = jwt_redis_blacklist.get(jti)
            return token_in_redis is not None
        except Exception as e:
            LOG.log_error(e)
        finally:
            return False
