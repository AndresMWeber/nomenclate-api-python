import datetime
from logging import getLogger
from mongoengine.errors import NotUniqueError, ValidationError
from marshmallow import fields
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from ..utils.responses import format_response, format_error
from .base import ApiRoute, validate_schema, BaseSchema

log = getLogger()


class EmailSchema(BaseSchema):
    email = fields.String(required=True)


class EmailPasswordSchema(EmailSchema):
    password = fields.String(required=True)


class NameEmailPasswordSchema(EmailPasswordSchema):
    name = fields.String(required=True)


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
            return format_error(str(e), 400)
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
        body = request.get_json()
        email = body.get("email")
        user = User.objects.get(email=email)
        if not user.active:
            return format_error("The specified user account is not active.", 401)
        if not user.check_password(body.get("password")):
            return format_error("Email or password invalid", 400)
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return format_response({"token": access_token}, 200)


class DeactivateApi(ApiRoute):
    @jwt_required()
    def post(self):
        user = User.objects.get(id=get_jwt_identity())
        if user:
            if not user.active:
                return format_error("User already deactivated", 409)
            user.deactivate()
            return format_response()
        return format_error(f"Logged in user not found.", status=404)


class ReactivateApi(ApiRoute):
    @jwt_required(optional=True)
    def post(self):
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
