from flask import Blueprint, request
from flask_login import login_user
from classes.user import User
from classes.db_queries import ConnectionInstance
from argon2 import PasswordHasher

login_func = Blueprint('login_func', __name__)
ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def check_password(password, username, app):
    with ConnectionInstance() as queries:
        return ph.verify(queries.get_pass_hash(username), password)


def get_user_id(username, app):
    with ConnectionInstance as queries:
        return queries.getUserId(username, app)


