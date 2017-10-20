from flask import Blueprint, request
from flask_login import login_user
from classes.user import User
from classes.db_queries import ConnectionInstance
from argon2 import PasswordHasher, exceptions

login_func = Blueprint('login_func', __name__)
ph = PasswordHasher()


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


