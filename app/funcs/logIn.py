from flask import Blueprint, request
from flask_login import login_user
from classes.user import User
from classes.db_queries import ConnectionInstance
from argon2 import PasswordHasher

login_func = Blueprint('login_func', __name__)
ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def check_password(password, email):
    with ConnectionInstance() as queries:
        if (queries.get_username(email)):
            return ph.verify(queries.get_pass_hash(email), password)
        else:  
            return False


def get_user_id(email):
    with ConnectionInstance as queries:
        return queries.getUserId(email)


