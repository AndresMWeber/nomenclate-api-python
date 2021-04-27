from .db import db
from flask_login import UserMixin, LoginManager
from flask_bcrypt import generate_password_hash, check_password_hash

login_manager = LoginManager()


class User(UserMixin, db.Document):
    meta = {"collection": "users"}
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
