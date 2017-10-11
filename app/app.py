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
from funcs.logIn import hash_password
import logging

app = Flask(__name__)
Mobility(app)

conf_file = 'cfg/db.json'

# Flask configuration parameters #
with open(conf_file, 'r') as cf:
    # Loads login information from file for security
    data = json.load(cf)
    app.config['DATABASE_USER'] = data['username']
    app.config['DATABASE_PASSWORD'] = data['password']
    app.config['DATABASE_DB'] = data['database']
    app.config['DATABASE_HOST'] = data['host']
app.config['shards'] = []  # Not actually sharding, just a handy way of keeping track of multiple connections
app.config['debug'] = True  # Testing only
app.secret_key = 'hella secret'
login_manager = LoginManager()
login_manager.init_app(app)

hash_password("password")

# TODO implement necessary loggers
# Hold off on this until we have more than one python file to work with to avoid having to rework logging
loggers = {}  # dict of loggers to init


@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


def setup_logging(log_name, log_file, log_level=logging.INFO):
    """
    :param log_name: String, descriptive name of log
    :param log_file: String, a path to .log file to write to
    :param log_level: logging.<PARAM>, INFO, DEBUG or WARNING, level of logging
    :return: log object, not necessary to use the returned object,
            but useful for storing logs in a list or dict for easier access
    """
    log = logging.getLogger(log_name)
    log.setLevel(log_level)
    handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='a')
    fmt = logging.Formatter('[%(asctime)s] :%(levelname)s: %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(fmt)
    log.addHandler(handler)
    return log


def end_logging(log):
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)


<<<<<<< HEAD
=======
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


def shard():
    # DEPRECATED, TO BE REMOVED
    shard = app.config['shards']
    app.config['shards'] += 1
    return shard


>>>>>>> ff0343f9123d58980b822bf10ae40ad5f279b1c6
##################################################################
# Some of the routes below might warrant moving out and
# into separate files, but until the scope of the operations
# that need to be performed are clear, they stay here
# as a skeleton for easy reference.
##################################################################

@app.route('/')
@mobile_template('/{mobile/}index.html')
def index(template):
<<<<<<< HEAD
=======
    log_basic()
>>>>>>> ff0343f9123d58980b822bf10ae40ad5f279b1c6
    # TODO fetch user data
    return render_template(template)


@app.route('/view/<calendar_id>')
@mobile_template('{mobile/}calendar.html')
def view(template, calendar_id):
<<<<<<< HEAD
    # TODO check if calendar exists and if the user has permission to view it
    # TODO create template and call render
    return render_template(template)
=======
    log_basic()
    with db.ConnectionInstance(app, shard()) as q:
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
>>>>>>> ff0343f9123d58980b822bf10ae40ad5f279b1c6


@app.route('/settings')
@mobile_template('{mobile/}template.html')
@login_required
def settings(template):
<<<<<<< HEAD
=======
    log_basic()
>>>>>>> ff0343f9123d58980b822bf10ae40ad5f279b1c6
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
    req_user = session['user']['id']
    del_user = request.form.get('user_id', None)
    if del_user and req_user == del_user:  # ensures only the user can delete themselves
        with db.ConnectionInstance(app) as q:
            q.db_del_user(del_user)
    return redirect(url_for(index))


@app.route('/delete_event', methods=['POST'])
@login_required
def delete_event():
    user = get_user_id()
    event = request.form.get('event_id', None)
    if event:
        with db.ConnectionInstance(app) as q:
            admins = q.db_get_cal_admin(eid=event)
            if user in admins:
                q.db_del_event(event)


@app.route('/delete_calendar', methods=['POST'])
@login_required
def delete_cal():
    user = session['user']['id']
    cal = request.form.get('calendar_id', None)
    if cal:
        with db.ConnectionInstance(app) as q:
            admins = q.db_get_cal_admin(cid=cal)
            if user in admins:
                q.db_del_cal(cal)

##################################################################


if __name__ == '__main__':

    active_loggers = []
    for log in loggers:
        lg = setup_logging(log, '{}.log'.format(log))
        active_loggers.append(lg)

    app.run()

    for log in active_loggers:
        end_logging(log)
