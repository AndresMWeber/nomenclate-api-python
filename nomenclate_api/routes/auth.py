from logging import getLogger
from mongoengine.errors import NotUniqueError, ValidationError
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from nomenclate_api.config import ACCESS_EXPIRES
from nomenclate_api.models.user import User
from nomenclate_api.db.blacklist import jwt_redis_blacklist
from nomenclate_api.utils.responses import format_response, format_error
from nomenclate_api.schemas import NameEmailPasswordSchema, EmailSchema, EmailPasswordSchema
from .base import ApiRoute, validate_schema


class SignupApi(ApiRoute):
    @validate_schema(NameEmailPasswordSchema())
    def post(self):
        """Sign up a new user
        ---
        schema:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: NameEmailPassword
            responses:
                201:
                    description: User created
                    content:
                        application/json:
                            schema: SignupResponse
                400:
                    description: There was a problem creating the user.
                    content:
                        application/json:
                            schema: ErrorSimple
                409:
                    description: That email address is already in use.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return format_response({"id": str(id)}, 201)
        except NotUniqueError:
            user = User.objects.get(email=body.get("email"))
            return format_error("That email address is already in use.", 409)
        except ValidationError as e:
            return format_error(e, 400)
        except Exception as e:
            self.log_error(f"Unhandled error creating user: {str(e)}")
            return format_error("There was a problem creating the user.", 400)


class UserExistsApi(ApiRoute):
    @validate_schema(EmailSchema())
    def post(self):
        """Does a given user exist
        ---
        schema:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: Email
            responses:
                200:
                    description: The requested user account exists.
                    content:
                        application/json:
                            schema: ExistsResponse
                404:
                    description: The requested user account does not exist.
                    content:
                        application/json:
                            schema: ExistsResponse
        """
        body = request.get_json()
        email = body.get("email")
        try:
            return format_response({"exists": bool(User.objects.get(email=email))}, 200)
        except:
            return format_response({"exists": False}, 404)


class LoginApi(ApiRoute):
    @validate_schema(EmailPasswordSchema())
    def post(self):
        """Log user in
        ---
        schema:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: EmailPassword
            responses:
                201:
                    description: Return a nomenclate object
                    content:
                        application/json:
                            schema: LoginResponse
                400:
                    description: Email or password invalid.
                    content:
                        application/json:
                            schema: ErrorSimple
                401:
                    description: The specified user account is not active.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        body = request.get_json()
        email = body.get("email")
        user = User.objects.get(email=email)
        if not user.active:
            return format_error("The specified user account is not active.", 401)
        if not user.check_password(body.get("password")):
            return format_error("Email or password invalid.", 400)
        access_token = create_access_token(identity=str(user.id), expires_delta=ACCESS_EXPIRES)
        return format_response({"token": access_token}, 200)


class LogoutApi(ApiRoute):
    @jwt_required()
    def post(self):
        """Log user out
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                200:
                    description: Successful logout
                400:
                    description: User is not logged in.
                400:
                    description: User login token expired.
                401:
                    description: The specified user account is not active.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        user = User.objects.get(id=get_jwt_identity())
        if not user.active:
            return format_error("The specified user account is not active.", 401)
        jti = get_jwt()["jti"]
        jwt_redis_blacklist.set(jti, "", ex=ACCESS_EXPIRES)
        return format_response("Access token revoked", 200)


class DeactivateApi(ApiRoute):
    @jwt_required()
    def post(self):
        """Deactivate user account
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                200:
                    description: Deactivated account successfully
                404:
                    description: Logged in user not found.
                409:
                    description: User already deactivated.
        """
        user = User.objects.get(id=get_jwt_identity())
        if user:
            if not user.active:
                return format_error("User already deactivated.", 409)
            user.deactivate()
            return format_response()
        return format_error("Logged in user not found.", status=404)


class ReactivateApi(ApiRoute):
    @validate_schema(EmailPasswordSchema())
    def post(self):
        """Reactivate user account
        ---
        schema:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: EmailPassword
            responses:
                200:
                    description: Reactivated account successfully
                200:
                    description: User already deactivated.
                401:
                    description: Incorrect username or password.
                404:
                    description: Logged in user not found.
        """
        body = request.get_json()
        email = body.get("email")
        password = body.get("password")
        user = User.objects.get(email=email)

        if not user.check_password(password):
            return format_error("Incorrect username or password.", 401)

        if user:
            if user.active:
                return format_response("Account already active.")
            user.activate()
            return format_response()

        return format_error(f"User with email {email} not found.", status=404)
