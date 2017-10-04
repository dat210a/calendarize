from flask import Flask, render_template, g, session, request, url_for, redirect
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from classes.user import User
from flask_login import *
from funcs.logIn import hash_password
import logging

app = Flask(__name__)
Mobility(app)

# Flask configuration parameters #
# TODO set database vars
app.config["DATABASE_USER"] = ""
app.config["DATABASE_PASSWORD"] = ""
app.config["DATABASE_DB"] = ""
app.config["DATABASE_HOST"] = ""
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


##################################################################
# Some of the routes below might warrant moving out and
# into separate files, but until the scope of the operations
# that need to be performed are clear, they stay here
# as a skeleton for easy reference.
##################################################################

@app.route('/')
@mobile_template('/{mobile/}index.html')
@login_required
def index(template):
    # TODO fetch user data
    return render_template(template)


@app.route('/view/<calendar_id>')
@mobile_template('{mobile/}calendar.html')
def view(template, calendar_id):
    # TODO check if calendar exists and if the user has permission to view it
    # TODO create template and call render
    pass


@app.route('/settings')
@mobile_template('{mobile/}template.html')
@login_required
def settings():
    # TODO load user's settings, then render a template with the settings
    pass


@app.route('/settings/save', methods=['POST'])  # <- could be done with AJAX?
def save_settings():
    # val = request.form.get(name_of_form_field, None) <- Syntax for getting form data
    # TODO extract settings from form and store in db
    return redirect(url_for(settings))  # reloads the settings page to show the new settings

##################################################################
# DELETION FUNCTIONS - emphasized because these not working
# properly is not good. Make sure to test properly.
# TODO remove emphasis only after these functions are tested


@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    # TODO rewrite if necessary when login functionality is implemented
    req_user = session['user']['id']
    del_user = request.form.get('user_id', None)
    if del_user and req_user == del_user:  # ensures only the user can delete themselves
        # TODO mark user as deleted in the database
        pass


@app.route('/delete_calendar', methods=['POST'])
@login_required
def delete_cal():
    user = session['user']['id']
    cal = request.form.get('calendar_id', None)
    if cal:
        # TODO
        # Make db request to check if user has permission to delete this calendar
        # Set calendar delete flag in db if yes
        pass

##################################################################


if __name__ == '__main__':

    active_loggers = []
    for log in loggers:
        lg = setup_logging(log, '{}.log'.format(log))
        active_loggers.append(lg)

    app.run()

    for log in active_loggers:
        end_logging(log)
