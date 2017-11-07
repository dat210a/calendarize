from classes.db_queries import ConnectionInstance
from flask_mail import Mail, Message
import json, string, random
from flask import Flask
app = Flask(__name__)

conf_file = "cfg/mail.json"
#Mail setup
with open(conf_file, 'r') as cf:
    # Loads mail configuration from file for security
    data = json.load(cf)
    app.config["MAIL_SERVER"] = data['server']
    app.config["MAIL_PORT"] = data['PORT']
    app.config["MAIL_USE_SSL"] = data['ssl']
    app.config['MAIL_USE_TLS'] = data['tls']
    app.config["MAIL_USERNAME"] = data['username']
    app.config["MAIL_PASSWORD"] = data['password']
mail = Mail(app)


sender = "dat210groupea@gmail.com"

def random_key(y):
    x = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(y)])
    return x

def send_verification(email,key):
    msg = Message("Verify your account",sender= sender,recipients=[ email ])
    msg.body = " Please click on the link below to verify your account:\n" + "http://localhost:5000/verify/"+ key
    mail.send(msg)
    return None

def send_recover(email):
    with ConnectionInstance() as queries:
        key = random_key(10) + str(queries.get_user_id(email))
        queries.make_resetkey(email,key)
    msg = Message("Reset Your password",sender=sender,recipients=[ email ])
    msg.body = " Please click on the link below to reset your password:\n" + "http://localhost:5000/reset/"+ key
    mail.send(msg)
    return None

def send_invite(sender_name,invited_email,calendar_name):
    msg = Message("Invitation to join "+ calendar_name + ".",sender=sender,recipients=[ invited_email ])
    msg.body = sender_name + " has invite you to join " + calendar_name +".\nVisit our webpage: http://localhost:5000"
    mail.send(msg)
    return None
