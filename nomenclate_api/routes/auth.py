import datetime
from logging import getLogger
from mongoengine.errors import NotUniqueError, ValidationError
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from nomenclate_api.models.user import User
from nomenclate_api.utils.responses import format_response, format_error
from nomenclate_api.api_spec import NameEmailPasswordSchema, EmailSchema, EmailPasswordSchema
from .base import ApiRoute, validate_schema

log = getLogger()


class SignupApi(ApiRoute):
    @validate_schema(NameEmailPasswordSchema())
    def post(self):
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
            log.error(f"Unhandled error creating user: {str(e)}")
            return format_error("There was a problem creating the user.", 400)


class UserExistsApi(ApiRoute):
    @validate_schema(EmailSchema())
    def post(self):
        body = request.get_json()
        email = body.get("email")
        try:
            bool(User.objects.get(email=email))
            return format_response({"exists": True}, 200)
        except:
            return format_response({"exists": False}, 404)


class LoginApi(ApiRoute):
    @validate_schema(EmailPasswordSchema())
    def post(self):
        """Log user in
        ---
        schema:
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
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return format_response({"token": access_token}, 200)


class DeactivateApi(ApiRoute):
    @jwt_required()
    def post(self):
        """Deactivate user account
        ---
        schema:
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
    @jwt_required(optional=True)
    def post(self):
        """Reactivate user account
        ---
        schema:
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
        user = None
        jwt = get_jwt_identity()
        if jwt:
            user = User.objects.get(id=jwt)
        else:
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
