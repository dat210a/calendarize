from flask import Blueprint, request
from flask_login import login_user
from classes.user import User
from classes.db_queries import ConnectionInstance
from argon2 import PasswordHasher

login_func = Blueprint('login_func', __name__)
ph = PasswordHasher()


def hash_password(password):
    print(ph.hash(password))
    return ph.hash(password)

def check_password(password, username, app):
    with ConnectionInstance(app , 1) as queries:
        return ph.verify(queries.get_pass_hash(username), hash_password(password))


def get_user_id(username, app):
    with ConnectionInstance as queries:
        return queries.getUserId(username, app)


@login_func.route("/login", methods=['POST'])
def login():
    password = request.form["password"]
    username = request.form["username"]

    if check_login(password, username):
        login_user(User(get_user_id(username)))



