import json, string, random
from classes.db_queries import ConnectionInstance
from flask_mail import Mail, Message
mail = Mail()

conf_file = "cfg/mail.json"
sender = "dat210groupea@gmail.com"

def init_mail(app):
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
    mail.init_app(app)

def random_key(y):
    x = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(y)])
    return x

def send_verification(email,key):
    try:
        msg = Message("Verify your account",sender= sender,recipients=[ email ])
        msg.body = " Please click on the link below to verify your account:\n" + "http://localhost:5000/verify/"+ key
        mail.send(msg)
        return True
    except:
        return False

def send_recover(email):
    with ConnectionInstance() as queries:
        key = random_key(10) + str(queries.get_user_id(email))
        queries.make_resetkey(email,key)
    try:
        msg = Message("Reset Your password",sender=sender,recipients=[ email ])
        msg.body = " Please click on the link below to reset your password:\n" + "http://localhost:5000/reset/"+ key
        mail.send(msg)
        return True
    except:
        return False

def send_invite(sender_name,invited_email,calendar_name):
    try:
        msg = Message("Invitation to join "+ calendar_name + ".",sender=sender,recipients=[ invited_email ])
        msg.body = sender_name + " has invited you to join " + calendar_name +".\nVisit our webpage: http://localhost:5000"
        mail.send(msg)
        return True
    except:
        return False

def send_bulk_calendar_invite(sender, emails):
    sent = []
    with mail.connect() as conn:
        for email in emails:
            try:
                msg = Message("Invitation to join "+ calendar_name + ".",sender=sender,recipients=[ invited_email ])
                msg.body = sender_name + " has invited you to join " + calendar_name +".\nVisit our webpage: http://localhost:5000"
                conn.send(msg)
                sent.append(email)
            except:
                pass
    return sent

def send_friend_request(sender, email):
    try:
        msg = Message("Friend request",sender=sender,recipients=[ email ])
        msg.body = sender + " has sent you a friend request on Calendarize.\nVisit our webpage: http://localhost:5000"
        mail.send(msg)
        return True
    except:
        return False


def send_bulk_friend_request(sender, emails):
    sent = []
    with mail.connect() as conn:
        for email in emails:
            try:
                msg = Message("Friend request",sender=sender,recipients=[ email ])
                msg.body = sender + " has sent you a friend request on Calendarize.\nVisit our webpage: http://localhost:5000"
                conn.send(msg)
                sent.append(email)
            except:
                pass
    return sent