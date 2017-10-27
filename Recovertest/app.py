from flask import Flask, request, render_template,g, redirect,url_for, flash, abort, session, make_response
import datetime
import random
import string
import mysql.connector
from flask_mail import Mail, Message
app = Flask(__name__)


app.secret_key = "any random string"
# Application config
app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "ABsolve123"
app.config["DATABASE_DB"] = "calendarize_db"
app.config["DATABASE_HOST"] = "localhost"
app.config["DEBUG"] = True  # only for development!

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = "465"
app.config["MAIL_USE_SSL"] = True
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USERNAME"] = "dat210groupea@gmail.com"
app.config["MAIL_PASSWORD"] = "48147640Aa"
app.config["DEBUG"] = True  # only for development!
mail = Mail(app)

def get_db():
    if not hasattr(g, "_database"):
        g.db = mysql.connector.connect(host=app.config["DATABASE_HOST"], user=app.config["DATABASE_USER"],
                                       password=app.config["DATABASE_PASSWORD"], database=app.config["DATABASE_DB"])
    return g.db

@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recover/", methods=["GET", "POST"])
def recover():
    if request.method=="POST":
        email = request.form.get("email", None)
        if not email:
            flash("You need to fill out an email!")
            return redirect(url_for('recover'))

        db = get_db()
        cur = db.cursor()
        try:
            qry = "select user_id from users where user_email=%s"
            cur.execute(qry, (email,))
            try:
                login_info = cur.fetchone()
                if not login_info:
                    flash("Unregistered Email")
                else:
                    # TODO: Generate random unique string for resetkey, store in database and send it along with the email.
                    x = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
                    key = x  + str(login_info[0])
                    db = get_db()
                    cur = db.cursor()
                    try:
                        qry1 = "update users set resetkey =%s, expires = now()+ interval 24 hour where user_email=%s"
                        cur.execute(qry1, (key,email,))
                        db.commit()
                        print(key)
                        msg = Message("Reset Your password",sender="dat210groupea@gmail.com",recipients=[ email ])
                        msg.body = " Please click on the link below to reset your password:\n" + "http://localhost:5000/reset/"+ key
                        mail.send(msg)
                    except:
                        pass
                    return render_template("recoverconfirm.html",email=email)
            except:
                pass
        finally:
            cur.close()

    return render_template("recover.html")

@app.route("/reset/<resetkey>", methods=["GET", "POST"])
def reset(resetkey):
    db = get_db()
    cur = db.cursor()
    try:
        qry1 = "select user_email, user_password from users where resetkey=%s and expires > now()"
        cur.execute(qry1, (resetkey,))
        info = cur.fetchone()
    finally:
        cur.close()
    if info:
        if request.method=="POST":
            new_password = request.form.get("new_password", None)
            repeat_password = request.form.get("repeat_password", None)
            if not new_password or not repeat_password:
                flash("Empty password")
            elif new_password == info[1]:
                flash("You cannot use the old password.")
            elif len(new_password) < 6:
                flash("Minimum 6 characters.")
            elif new_password == repeat_password:
                db = get_db()
                cur = db.cursor()
                try:
                    qry = "update users set user_password =%s, resetkey='' where user_email = '" + info[0] +"'"
                    cur.execute(qry, (new_password,))
                    db.commit()
                finally:
                    cur.close()
                    return render_template("resetsuccess.html")
            else:
                flash("Your password do not match")
        return render_template("reset.html")
    else:
        return render_template("invalidlink.html")


if __name__ == "__main__":
    app.run()
