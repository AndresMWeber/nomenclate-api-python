from redis import StrictRedis
from flask import session
from nomenclate_api.config import ACCESS_EXPIRES, LOG, REDIS_HOST, REDIS_PASS, REDIS_PORT

jwt_redis_blacklist = None


def blacklist_token(token):
    try:
        session.set(token, "", ex=ACCESS_EXPIRES)
    except Exception as e:
        LOG.debug(e)


def init_blacklist(app, jwt):
    jwt_redis_blacklist = None
    if REDIS_PASS and REDIS_HOST and REDIS_PORT:
        try:
            jwt_redis_blacklist = StrictRedis(
                host=REDIS_HOST, password=REDIS_PASS, port=REDIS_PORT, db=0, decode_responses=False
            )
            app.config["SESSION_REDIS"] = jwt_redis_blacklist
            app.config["SESSION_TYPE"] = "redis"
        except:
            LOG.log_error("Could not connect to redis.")

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(_, jwt_payload):
        try:
            jti = jwt_payload["jti"]
            token_in_redis = session.get(jti)
            return token_in_redis is not None
        except Exception as e:
            LOG.log_error(e)
        finally:
            return False

    return jwt_redis_blacklist
