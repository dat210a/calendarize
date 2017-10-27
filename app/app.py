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
import json, datetime
from classes import db_queries as db
from flask import Flask, flash, render_template, session, g, request, url_for, redirect
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from classes.user import User
from flask_login import *
from flask_login import login_user, current_user
from funcs.logIn import check_password, hash_password
from funcs.logIn import login_func
from funcs import file_tools


# app initialization
app = Flask(__name__)
Mobility(app)

# config setup
app.config['DEBUG'] = True  # Testing only

# needed for session cookies
app.secret_key = 'hella secret'

# initialization of login manager
# it keeps the given user logged in via use of cookies
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

# stores returned user into current session
@login_manager.user_loader
def load_user(email):
    """Returns an object of class User based on provided unique identifier
       if user in the database, otherwise None
    """
    if user_exists(email):
        return User(email)
    return None



def setup_logging():
    """
    """
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
    """
    """
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)


def request_data(req):
    """
    """
    res = '{} requested by {}'.format(req.url, req.remote_addr)
    return res


def log_basic():
    """
    """
    # This handles logging of basic data that should be logged for all requests
    if logger:
        logger.info(request_data(request))


def get_user_id():
    """
    """
    if 'user' in session:
        return session['user']['id']
    return None

# It should be moved to a separate file if there 
# ends up being more functions like this one
def user_exists(email):
    """Returnes True if user with provided identifier exists, 
       otherwise False                     
    """
    with db.ConnectionInstance() as queries:
        if queries.get_username(email) is None:
            return False
        return True


##################################################################

# Some of the routes below might warrant moving out and
# into separate files, but until the scope of the operations
# that need to be performed are clear, they stay here
# as a skeleton for easy reference.
# #################################################################

@app.route('/')
@mobile_template('/{mobile/}index.html')
def index(template):
    """
    """
    log_basic()
#    from classes.dummy_classes import ShardTestingClass
#    for i in range(0, 5):
#        with ShardTestingClass(app) as st:
#            print(app.config['shards'])
#            st.work()
#        print(app.config['shards'])
    if (current_user.is_authenticated):
        return redirect('/user_index')
    return render_template(template)


@app.route('/user_index')
@mobile_template('/{mobile/}user_index.html')
@login_required
def user_index(template):
    """
    """
    log_basic()
#    from classes.dummy_classes import ShardTestingClass
#    for i in range(0, 5):
#        with ShardTestingClass(app) as st:
#            print(app.config['shards'])
#            st.work()
#        print(app.config['shards'])
    return render_template(template, name=current_user.username)


@app.route('/user_availability', methods=['GET', 'POST'])
def user_availability():
    """
    """
    if request.method == "POST":
        email = request.form['inputEmail']
        if email and user_exists(email):
            return 'false'
        return 'true'
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    """
    if request.method == "POST":
        # read the posted values from the UI
        name = request.form['inputUsername']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        # validate received values
        if name and email and password and not user_exists(email):
            with db.ConnectionInstance() as queries:
                #adds new user to the database
                added = queries.add_user(name, email, hash_password(password))
                if (added):
                    user = User(email)
                    login_user(user)
                    #adds default calendar to that user
                    queries.add_calendar(datetime.datetime.utcnow(), current_user.user_id)
                    return redirect('/calendar')
    # reload if something not right
    # TODO maybe some error messages
    return redirect('/')


@app.route('/verify_credentials', methods=['GET', 'POST'])
def verify_credentials():
    """
    """
    if request.method == "POST":
        email = request.form['inputEmail']
        password = request.form["inputPassword"]
        if email and user_exists(email) and check_password(password, email):
            return 'true'
        return 'false'
    return redirect('/')


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    """
    if request.method == "POST":
        password = request.form["inputPassword"]
        email = request.form["inputEmail"]
        user = load_user(email)
        if user is not None:
            if check_password(password, email):
                if 'remember' in request.form and request.form["remember"] == 'on':
                    remember_me = True
                else: 
                    remember_me = False
                login_user(user, remember=remember_me)
                return redirect('/user_index')
    return redirect('/')


@app.route("/logout")
@login_required
def logout():
    """ Logs user out and redirects to main page
    """
    logout_user()
    return redirect('/')


@app.route('/calendar')
@mobile_template('/{mobile/}calendar.html')
@login_required
def calendar(template):
    """
    """
    log_basic()
    return render_template(template, name=current_user.username)


@app.route('/get_data')
@login_required
def get_data():
    """
    """
    log_basic()
    with db.ConnectionInstance() as queries:
        results = queries.fetch_data_for_display(current_user.user_id)       
    return json.dumps(results, default=type_handler)


# should be moved to funcs/helper.py
def type_handler(x):
    if isinstance(x, datetime.date):
        # TODO change date into clients time zone
        return x.isoformat()
    elif isinstance(x, bytearray):
        return x.decode('utf-8')
    raise TypeError("Unknown type")


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


@app.route('/add_calendar', methods=['POST'])
@login_required
def add_calendar():
    cal_name = request.form['newCalendarName']
    if cal_name:
        with db.ConnectionInstance() as queries:
            created = queries.add_calendar(datetime.datetime.utcnow(), current_user.user_id, cal_name)
            if created:
                return 'true'
    return 'false'


@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    data = request.form
    if data['newEventName'] and data['calendarID'] and data['startDate']:
        # TODO conversion of dates into right format if they are not and into utc
        # TODO check that startDate <= endDate
        with db.ConnectionInstance() as queries:
            created = queries.add_event(request.form, datetime.datetime.utcnow(), current_user.user_id)
            print (created)
            if created:
                return 'true'
    return 'false'


@app.route('/add_files', methods=['POST'])
@login_required
def add_files():
    print (request.form)
    print (request.files)
    return 'true'


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
