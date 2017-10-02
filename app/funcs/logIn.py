from flask import Blueprint, request
from flask_login import login_user
from app.classes.user import User

login_func = Blueprint('login_func', __name__)


def hash_password(password):
    return 5


def check_login(password, username):
    password = hash_password(password)


def get_user_id(username):
    return "test"


@login_func.route("/login", methods=['POST'])
def login():
    password = request.form["password"]
    username = request.form["username"]

    if check_login(password, username):
        login_user(User(get_user_id(username)))


