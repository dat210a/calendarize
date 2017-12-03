from flask import Blueprint, request, flash, render_template, redirect, url_for
from classes import db_queries as db
from flask_login import login_user
from funcs.logIn import user_exists, load_user
from funcs.send_email import send_verification, random_key, send_recover
from funcs.reset import reset_password

verifyAndRecover = Blueprint('verifyAndRecover', __name__,
                        template_folder='templates')


@verifyAndRecover.route("/recover/", methods=["GET", "POST"])
def recover():
    if request.method=="POST":
        email = request.form.get("email", None)
        if not email:
            flash("You need to fill out an email!")
            return redirect(url_for('recover'))
        if user_exists(email):
            send_recover(email)
            return render_template("recoverconfirm.html",email=email)
        else:
            return render_template("recoverconfirm.html",email=email)
    return render_template("recover.html")


@verifyAndRecover.route("/reset/<resetkey>", methods=["GET", "POST"])
def reset(resetkey):
    with db.ConnectionInstance() as queries:
        email = queries.get_reset_info(resetkey)
    if email:
        if request.method =="POST":
            if reset_password(email):
                return render_template("resetsuccess.html")
        return render_template("reset.html")
    else:
        return render_template("invalidlink.html")


@verifyAndRecover.route("/verify/<verify_key>", methods=["GET", "POST"])
def verify(verify_key):
    with db.ConnectionInstance() as queries:
        email = queries.get_verify_info(verify_key)
    if email:
        with db.ConnectionInstance() as queries:
            queries.activate_user(email)
            user = load_user(email)
            login_user(user)
        return render_template("verify_confirm.html")
    else:
        return ("Your account has been already verified or the link is no longer valid")


@verifyAndRecover.route("/verifyoption", methods=["GET", "POST"])
def verifyoption():
    email = request.form.get("email", None)
    user = load_user(email)
    if email:
        key = random_key(10) + email
        with db.ConnectionInstance() as queries:
            queries.make_verifykey(user.user_id,key)
        send_verification(email,key)
        return render_template("verify_send.html", email=email)