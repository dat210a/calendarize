from flask import Blueprint, request
from flask_login import LoginManager, login_user, current_user
from classes.user import User
from classes.db_queries import ConnectionInstance
from argon2 import PasswordHasher, exceptions

login_func = Blueprint('login_func', __name__)
ph = PasswordHasher()

# initialization of login manager
# it keeps the given user logged in via use of cookies
login_manager = LoginManager()
login_manager.login_view = '/'

def init_login(app):
    login_manager.init_app(app)

# stores returned user into current session
@login_manager.user_loader
def load_user(email):
    """Returns an object of class User based on provided unique identifier
       if user in the database, otherwise None
    """
    if user_exists(email):
        return User(email)
    return None


def user_exists(email):
    """Returnes True if user with provided identifier exists,
       otherwise False
    """
    with ConnectionInstance() as queries:
        if queries.get_user_id(email) is None:
            return False
        return True


def hash_password(password):
    return ph.hash(password)


def check_password(password, email):
    with ConnectionInstance() as queries:
        try:
            return ph.verify(queries.get_pass_hash(email), password)
        except exceptions.VerifyMismatchError:
            return False


def get_user_id(email):
    with ConnectionInstance as queries:
        return queries.getUserId(email)


