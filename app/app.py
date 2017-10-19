"""
calendarize Flask application file

The code for this project loosely follows PEP 8 style guidelines.
You can read about them here: https://www.python.org/dev/peps/pep-0008/
Any code that does not comply will be modified to do so if possible.
If you're using PyCharm, it will have built-in PEP8 linting,
and similar packages should be available for other editors.

Links to documentation for the packages used can be found
in the GitHub repository README.md

"""
import logging
import json
from classes import db_queries as db
from flask import Flask, render_template, g, session, request, url_for, redirect
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from classes.user import User
from flask_login import *
from flask_login import login_user, current_user
from funcs.logIn import check_password, hash_password
from funcs.logIn import login_func

app = Flask(__name__)
Mobility(app)


@app.before_request
def make_session_permanent():
    session.permanent = False


app.config['debug'] = True  # Testing only
app.secret_key = 'hella secret'
app.config['PERMANENT_SESSION_LIFETIME']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'


@login_manager.user_loader
def load_user(email):
    with db.ConnectionInstance() as q:
        if q.get_username(email) is None:
            return None
    return User(email)


def setup_logging():
    try:
        lg = logging.getLogger(__name__)
        lg.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='calendarize.log', encoding='utf-8', mode='a')
        fmt = logging.Formatter('[%(asctime)s]:%(module)s:%(levelname)s: %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(fmt)
        lg.addHandler(handler)
        return lg
    except PermissionError as e:
        print('{}\n'
              'WARNING: Logging not enabled.\n'
              'If you get this error, change your IDE working directory.\n'
              'The application will still work, but nothing will be logged.'.format(e))
        # In PyCharm, go to Run>Edit Configuration to set the working directory to the calendarize folder.


def end_logging(log):
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)


def request_data(req):
    res = '{} requested by {}'.format(req.url, req.remote_addr)
    return res


def log_basic():
    # This handles logging of basic data that should be logged for all requests
    if logger:
        logger.info(request_data(request))


def get_user_id():
    if 'user' in session:
        return session['user']['id']
    return None


##################################################################

# Some of the routes below might warrant moving out and
# into separate files, but until the scope of the operations
# that need to be performed are clear, they stay here
# as a skeleton for easy reference.
# #################################################################

@app.route('/')
@mobile_template('/{mobile/}index.html')
# @login_required
def index(template):
    print (session)
    log_basic()
#    from classes.dummy_classes import ShardTestingClass
#    for i in range(0, 5):
#        with ShardTestingClass(app) as st:
#            print(app.config['shards'])
#            st.work()
#        print(app.config['shards'])
    # TODO fetch user data
    return render_template(template)


#temorary
@app.route('/calendar')
@mobile_template('/{mobile/}calendar.html')
@fresh_login_required
def calendar(template):
    log_basic()
    # TODO fetch user data
    return render_template(template, name=current_user.username)


@app.route('/register', methods=['POST'])
def register():
    # read the posted values from the UI
    _name = request.form['inputUsername']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    # validate the received values
    if _name and _email and _password:
        with db.ConnectionInstance() as q:
            if q.get_username(_email) == None:
                added = q.add_user(_name, _email, hash_password(_password))
                if (added):
                    user = User(_email)
                    login_user(user)
                    return json.dumps({'success':True})
                else:
                    return json.dumps({"message": "Could not add a new user at this time, try again later."})
            else:
                return json.dumps({"message": "User with this email address already exists"})
    else:
        return json.dumps({"message": "Missing or invalid data"})


@app.route("/login", methods=['POST'])
def login():
    password = request.form["inputPassword"]
    email = request.form["inputEmail"]
    user = load_user(email)
    if user is not None:
        if check_password(password, email):
            login_user(user)
            return json.dumps({'success':True})
    return json.dumps({'message':'Wrong email or password'})


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')
    


@app.route('/view/<calendar_id>')
@mobile_template('{mobile/}calendar.html')
def view(template, calendar_id):
    log_basic()

    with db.ConnectionInstance() as q:

        cals = q.get_calendars()
        if calendar_id in cals:
            members = q.get_calendar_members(calendar_id)
            if get_user_id() in members:
                # TODO create template
                return render_template(template)
            else:
                # return redirect(url_for(error))
                pass
        else:
            # return redirect(url_for(error))
            # TODO create error route, uncomment above lines
            pass


@app.route('/settings')
@mobile_template('{mobile/}template.html')
@login_required
def settings(template):
    log_basic()
    # TODO load user's settings, then render a template with the settings
    return render_template(template)


@app.route('/settings/save', methods=['POST'])  # <- could be done with AJAX?
def save_settings():
    # val = request.form.get(name_of_form_field, None) <- Syntax for getting form data
    # TODO extract settings from form and store in db
    return redirect(url_for(settings))  # reloads the settings page to show the new settings

##################################################################
# DELETION FUNCTIONS - emphasized because these not working
# properly is not good. Make sure to test properly.
# TODO remove emphasis only after these functions are tested
# TODO errors and error handling


@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    # TODO rewrite if necessary when login functionality is implemented
    req_user = get_user_id()
    del_user = request.form.get('user_id', None)
    if del_user and req_user == del_user:  # ensures only the user can delete themselves
        with db.ConnectionInstance() as q:
            q.db_del_user(del_user)
    return redirect(url_for(index))


@app.route('/delete_event', methods=['POST'])
@login_required
def delete_event():
    user = get_user_id()
    event = request.form.get('event_id', None)
    if event:
        with db.ConnectionInstance() as q:
            admins = q.db_get_cal_admin(eid=event)
            if user in admins:
                q.db_del_event(event)


@app.route('/delete_calendar', methods=['POST'])
@login_required
def delete_cal():
    user = get_user_id()
    cal = request.form.get('calendar_id', None)
    if cal:
        with db.ConnectionInstance() as q:
            admins = q.db_get_cal_admin(cid=cal)
            if user in admins:
                q.db_del_cal(cal)
    


##################################################################


if __name__ == '__main__':

    logger = setup_logging()

    app.run()

    end_logging(logger)
