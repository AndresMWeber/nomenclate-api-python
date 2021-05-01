from flask_login import UserMixin, LoginManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from nomenclate_api.db.config import db

login_manager = LoginManager()


class User(UserMixin, db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    active = db.BooleanField(default=True)
    config = db.ReferenceField("Config")
    meta = {"collection": "users"}

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    @classmethod
    def get_from_jwt(cls):
        try:
            return cls.objects.get(id=get_jwt_identity())
        except:
            return None


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
