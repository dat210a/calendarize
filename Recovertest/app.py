from flask import Flask, request, render_template,g, redirect,url_for, flash, abort, session, make_response
import datetime
import mysql.connector
from flask_mail import Mail, Message
app = Flask(__name__)

app.secret_key = "any random string"
# Application config
app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "-------"
app.config["DATABASE_DB"] = "recovertest"
app.config["DATABASE_HOST"] = "localhost"
app.config["DEBUG"] = True  # only for development!

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = "465"
app.config["MAIL_USE_SSL"] = True
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USERNAME"] = "dat210groupea@gmail.com"
app.config["MAIL_PASSWORD"] = "------"
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
            return redirect(url_for("recover"))

        db = get_db()
        cur = db.cursor()
        try:
            qry = "select user, password from users where email=%s"
            cur.execute(qry, (email,))
            try:
                login_info = cur.fetchone()
                if not login_info:
                    flash("Unregistered Email")
                    return redirect(url_for("recover"))
                else:
                    msg = Message("Reset Your password",sender="dat210groupea@gmail.com",recipients=["g_natdanai@hotmail.com"])
                    msg.body = " Please click on the link below to reset your password:\n" + "http://localhost:5000/reset"
                    mail.send(msg)
                    return render_template("recoverconfirm.html",email=email)
            except:
                pass
        finally:
            cur.close()

    return render_template("recover.html")

@app.route("/reset/<resetlink>", methods=["GET", "POST"])
def reset(resetlink):
    return render_template("reset.html")


if __name__ == "__main__":
    app.run()
