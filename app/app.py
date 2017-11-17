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
import json, string, re, random
import pytz
# from pytz import timezone
from datetime import datetime, date
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
from flask_mail import Mail, Message
from funcs.file_tools import load_file
from funcs.send_email import *
from funcs.reset import *
from views.sidebar import sidebar

# app initialization
app = Flask(__name__)
app.register_blueprint(sidebar.sidebar, url_prefix='/side')
Mobility(app)

# config setup
app.config['DEBUG'] = True  # Testing only

# needed for session cookies
app.secret_key = 'hella secret'
mail = Mail(app)

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


logger = setup_logging()


@app.before_request
def prequest():
    log_basic()


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


# It should be moved to a separate file if there
# ends up being more functions like this one
def user_exists(email):
    """Returnes True if user with provided identifier exists,
       otherwise False
    """
    with db.ConnectionInstance() as queries:
        if queries.get_user_id(email) is None:
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
#    from classes.dummy_classes import ShardTestingClass
#    for i in range(0, 5):
#        with ShardTestingClass(app) as st:
#            print(app.config['shards'])
#            st.work()
#        print(app.config['shards'])
    if (current_user.is_authenticated):
        return redirect('/index_user')
    return render_template(template)


@app.route('/index_user')
@mobile_template('/{mobile/}index_user.html')
@login_required
def index_user(template):
    """
    """
#    from classes.dummy_classes import ShardTestingClass
#    for i in range(0, 5):
#        with ShardTestingClass(app) as st:
#            print(app.config['shards'])
#            st.work()
#        print(app.config['shards'])
    return render_template(template, name=current_user.username())


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
        email = request.form.get('inputEmail', None)
        password = request.form.get('inputPassword', None)
        # validate received values
        if email and password and not user_exists(email):
            with db.ConnectionInstance() as queries:
                key = random_key(10) + email[:5]
                # TODO delete or merge previously created user if exists
                #adds new user to the database
                added = queries.add_user(datetime.utcnow(), email, hash_password(password),key)
                if (added):
                    user = User(email)
                    #adds default calendar to that user
                    queries.add_calendar(datetime.utcnow(), user.user_id)
                    #send verfication email
                    send_verification(email,key)
                    return render_template("verify_send.html", email=email)
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
            if not user.is_active():
                return render_template("verify_option.html", email=email)
            if check_password(password, email) and user.is_active():
                if 'remember' in request.form and request.form["remember"] == 'on':
                    remember_me = True
                else:
                    remember_me = False
                login_user(user, remember=remember_me)
                return redirect('/index_user')
    return redirect('/')


@app.route("/logout")
@login_required
def logout():
    """ Logs user out and redirects to main page
    """
    logout_user()
    # TODO redirect to: you have been successfully logged out
    return redirect('/')


@app.route("/recover/", methods=["GET", "POST"])
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


@app.route("/reset/<resetkey>", methods=["GET", "POST"])
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

@app.route('/calendar')
@mobile_template('/{mobile/}calendar.html')
@login_required
def calendar(template):
    """
    """
    with db.ConnectionInstance() as queries:
        invites = queries.get_user_invites(current_user.user_id)
        invites = len(invites) if invites else 0
    return render_template(template, name=current_user.username(), notifier=invites)


@app.route('/get_data')
@login_required
def get_data():
    """
    """
    with db.ConnectionInstance() as queries:
        calendar_ids = queries.get_calendars(current_user.user_id)
        cal_details = queries.get_calendars_details(calendar_ids)
        event_details = queries.get_events_details(calendar_ids)
    return json.dumps([cal_details, event_details], default=type_handler)


# helper function, should be moved
def type_handler(x):
    if isinstance(x, (date, datetime)):
        x = pytz.utc.localize(x)
        # TODO if desired timezone set use this line:
        # x = x.astimezone(tz)
        return x.isoformat()
    elif isinstance(x, bytearray):
        return x.decode('utf-8')
    raise TypeError("Unknown type")


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    eid = request.args.get('id', None)
    chid = request.args.get('chid', None)
    with db.ConnectionInstance() as queries:
        cal = queries.get_event_calendar_id(eid)
        role = queries.get_calendar_role(current_user.user_id, cal)
        if role is not None:
            return load_file(filename, eid, chid)
    # return redirect(url_for('error'))


@app.route('/add_calendar', methods=['POST', 'GET'])
@login_required
def add_calendar():
    if request.method == "POST":
        cal_name = request.form.get('newCalendarName', None)
        cal_color = request.form.get('color', None)
        if cal_name and cal_color and len(cal_name) < 45 and len(cal_color) == 7:
            with db.ConnectionInstance() as queries:
                new_cal_id = queries.add_calendar(datetime.utcnow(), current_user.user_id, cal_name, cal_color[1:])
                if new_cal_id:
                    # parse 'invites' string and send invites
                    invites = re.sub( '\s+', ' ', request.form.get('invites', '')).strip()
                    invites = re.split(',| |;', invites)
                    for email in invites:
                        if '@' in email and queries.check_invite(email, new_cal_id):
                            role = 3 # 0: owner, 1: admin, 2: contributor, 3: user
                            queries.send_invite(new_cal_id, queries.get_user_id(email), current_user.user_id, role, email)
                            sender = current_user.username()
                            # send email to email
                            send_invite(sender,email,cal_name)
                    cal_data = queries.get_calendars_details((new_cal_id,))[0]
                    return json.dumps({'success' : 'true', 'data' : json.dumps(cal_data, default=type_handler)})
    return json.dumps({'success' : 'false'})


@app.route('/request_calandar', methods=['POST', 'GET'])
@login_required
def request_calandar():
    if request.method == "POST":
        cal_id = request.form.get('cal_id', None)
        if cal_id:
            with db.ConnectionInstance() as queries:
                role = queries.get_calendar_role(current_user.user_id, cal_id)
                if role is not None:
                    cal_data = queries.get_calendars_details((cal_id,))[0]
                    return json.dumps({'success' : 'true', 'data' : json.dumps(cal_data, default=type_handler)})
    return json.dumps({'success' : 'false'})


@app.route('/join_calander', methods=['POST', 'GET'])
@login_required
def join_calander():
    if request.method == 'POST':
        id = request.form.get("calendar_id", None)
        role = request.form.get("role", None)
        with db.ConnectionInstance() as q:
            if q.check_for_invite(current_user.user_id, id, role) == True:
                q.join_calander(id, current_user.user_id, role)
                return 'true'
    return 'false'


@app.route('/decline_calander', methods=['POST', 'GET'])
@login_required
def decline_calander():
    if request.method == 'POST':
        id = request.form.get("calendar_id", None)
        role = request.form.get("role", None)
        with db.ConnectionInstance() as q:
            if q.check_for_invite(current_user.user_id, id, role) == True:
                return 'true'
    return 'false'


@app.route('/invite_calendar', methods=['POST', 'GET'])
@login_required
def invite_calander():
    if request.method == 'POST':
        email = request.form.get("email", None)
        if len(email) > 45:
            return 'false'
        calendar_id = request.form.get("calendar_id", None)
        role = request.form.get("role", None)
        with db.ConnectionInstance() as q:
            if q.get_calendar_role(current_user.user_id, calendar_id) == 0 and q.check_invite(email, calendar_id):
                q.send_invite(calendar_id, q.get_user_id(email), current_user.user_id, role, email)
                return 'true'
    return 'false'


@app.route('/leave_calander', methods=['POST', 'GET'])
@login_required
def leave_calander():
    if request.method == 'POST':
        id = request.form.get("calender_id", None)
        with db.ConnectionInstance() as q:
            q.leave_calander(id, current_user.user_id)
        return 'true'
    return 'false'


@app.route('/add_event', methods=['POST', 'GET'])
@login_required
def add_event():
    if request.method == "POST":
        response, data = prepare_new_event_data()
        if not response:
            return json.dumps({'success' : 'false', 'message': data})
        with db.ConnectionInstance() as queries:
            role = queries.get_calendar_role(current_user.user_id, data['event_calendar_id'])
            if role is not None and role <= 2:
                eid = queries.add_event(data)
                if eid:
                    success = [queries.add_event_file(file, eid) for file in request.files.getlist('file')]
                    return json.dumps({'success' : 'true', 'id': eid, 'files': success})
    return json.dumps({'success' : 'false'})


def prepare_new_event_data():
    data = {}
    data['event_name'] = request.form.get('newEventName', None)
    data['event_calendar_id'] = request.form.get('calendarID', None)
    if not data['event_name'] or not data['event_calendar_id']:
        return False, 'basic information'
    try:
        data['event_start'] = datetime.utcfromtimestamp(int(request.form['startDate'])/1000.0)
    except:
        return False, 'date'
    try:
        data['event_end'] = datetime.utcfromtimestamp(int(request.form['endDate'])/1000.0)
        if data['event_end'] < data['event_start']:
            data['event_end'] = data['event_start']
    except:
        data['event_end'] = data['event_start']
    data['event_date_created'] = datetime.utcnow()
    data['event_owner_id'] = current_user.user_id
    data['event_recurring'] = 1 if 'recurring' in request.form else 0
    data['event_fixed_date'] = 1 if 'fixedSwitch' in request.form else 0
    data['event_details'] = request.form.get('event_details', None)
    return True, data


@app.route('/edit_event', methods=['POST', 'GET'])
@login_required
def edit_event():
    if request.method == "POST":
        eid = request.form.get('event_id', None)
        if eid is None:
            return json.dumps({'success' : 'false', 'message': 'Missing event id'})

        response, data = prepare_edit_event_data()
        if not response:
            return json.dumps({'success' : 'false', 'message': data})

        with db.ConnectionInstance() as queries:
            current_calendar = queries.get_event_calendar_id(eid)
            if current_calendar is None:
                return json.dumps({'success' : 'false', 'message': 'bad event ID'})

            role_old = queries.get_calendar_role(current_user.user_id, current_calendar)
            if role_old is None or role_old > 1:
                return json.dumps({'success' : 'false', 'message': 'no permission'})

            if data['event_calendar_id'] and data['event_calendar_id'] != current_calendar:
                role_new = queries.get_calendar_role(current_user.user_id, data['event_calendar_id'])
                if role_new is None or role_new > 1:
                    return json.dumps({'success' : 'false', 'message': 'no permission'})

            edit = queries.update_event(data, eid)
            if edit:
                success = [queries.add_event_file(file, eid) for file in request.files.getlist('file')]
                return json.dumps({'success' : 'true', 'files': success})

    return json.dumps({'success' : 'false'})


def prepare_edit_event_data():
    data = {}
    name = request.form.get('newEventName', None)
    if name:
        data['event_name'] = name
    cal = request.form.get('calendarID', None)
    if cal:
        data['event_calendar_id'] = cal
    try:
        data['event_start'] = datetime.utcfromtimestamp(int(request.form['startDate'])/1000.0)
        data['event_end'] = datetime.utcfromtimestamp(int(request.form['endDate'])/1000.0)
        if data['event_end'] < data['event_start']:
            data['event_end'] = data['event_start']
    except:
        pass
    data['event_recurring'] = 1 if 'recurring' in request.form else 0
    data['event_fixed_date'] = 1 if 'fixedSwitch' in request.form else 0
    data['event_details'] = request.form.get('event_details', None)
    return True, data


@app.route('/set_instance', methods=['POST', 'GET'])
@login_required
def set_instance():
    print(request.form)
    if request.method == "POST":
        eid = request.form.get('event_id', None)
        year = request.form.get('year', None)
        if not eid or not year:
            return json.dumps({'success' : 'false', 'message': 'Non specified event id or year'})

        response, data = prepare_set_instance_data()
        if not response:
            return json.dumps({'success' : 'false', 'message': data})

        with db.ConnectionInstance() as queries:
            cid = queries.get_event_calendar_id(eid)
            role = queries.get_calendar_role(current_user.user_id, cid)
            if role is not None and role <= 2:
                chid = queries.get_child_id(eid, year)
                if chid:
                    queries.update_child(data, iid)
                else:
                    data['child_date_created'] = datetime.utcnow()
                    data['child_owner_id'] = current_user.user_id
                    data['child_parent_id'] = eid
                    data['child_year'] = year
                    chid = queries.add_child(data)
                if chid:
                    success = [queries.add_child_file(file, eid, chid) for file in request.files.getlist('file')]
                    return json.dumps({'success' : 'true', 'files': success})
    return json.dumps({'success' : 'false'})


def prepare_set_instance_data():
    data = {}
    try:
        data['child_start'] = datetime.utcfromtimestamp(int(request.form['startDate'])/1000.0)
    except:
        return False, 'date'
    try:
        data['child_end'] = datetime.utcfromtimestamp(int(request.form['endDate'])/1000.0)
        if data['child_end'] < data['child_start']:
            data['child_end'] = data['child_start']
    except:
        data['child_end'] = data['child_start']
    data['child_fixed_date'] = 1 if 'fixedSwitch' in request.form else 0
    data['child_details'] = request.form.get('event_details', None)
    return True, data


# @app.route('/add_files', methods=['POST'])
# @login_required
# def add_files():
#     with db.ConnectionInstance() as q:
#         for file in request.files:
#             success = q.add_file(request.files[file], request.form['event_id'])
#             if not success:
#                 # TODO handle what happens if the file fails to upload
#                 pass
#     return 'true'


@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == "POST":
        name = request.form.get('name', None)
        name = current_user.name if name == '' or name == None else name
        try:
            phone = int(request.form['phone'])
        except:
            phone = None
        if name and len(name) < 45:
            with db.ConnectionInstance() as queries:
                if queries.update_user(current_user.user_id, name, phone):
                    return 'true'
    return 'false'


##################################################################
# DELETION FUNCTIONS - emphasized because these not working
# properly is not good. Make sure to test properly.
# TODO remove emphasis only after these functions are tested
# TODO errors and error handling


@app.route('/delete_user')
@fresh_login_required
def delete_user():
    with db.ConnectionInstance() as queries:
        queries.db_del_user(current_user.user_id)
        logout_user()
        # TODO redirect to user has been deleted page
    return redirect(url_for('index'))


@app.route('/delete_event', methods=['POST', 'GET'])
@fresh_login_required
def delete_event():
    if request.method=="POST":
        event = request.form.get('event_id', None)
        if event:
            with db.ConnectionInstance() as queries:
                cal = queries.get_event_calendar_id(event)
                role = queries.get_calendar_role(current_user.user_id, cal)
                if role is not None and role == 0:
                    queries.db_del_event(event)
                    # TODO delete files
                    return 'true'
    return 'false'


@app.route('/delete_instance', methods=['POST', 'GET'])
@fresh_login_required
def delete_instance():
    if request.method=="POST":
        event = request.form.get('event_id', None)
        year = request.form.get('year', None)
        if event and year:
            with db.ConnectionInstance() as queries:
                cal = queries.get_event_calendar_id(event)
                role = queries.get_calendar_role(current_user.user_id, cal)
                if role is not None and role < 2:
                    queries.db_del_child(event, year)
                    # TODO delete files
                    return 'true'
    return 'false'


@app.route('/delete_calendar', methods=['POST', 'GET'])
@fresh_login_required
def delete_cal():
    if request.method=="POST":
        cal = request.form.get('calendar_id', None)
        if cal:
            with db.ConnectionInstance() as queries:
                role = queries.get_calendar_role(current_user.user_id, cal)
                if role is not None and role == 0:
                    queries.db_del_cal(cal)
                    return 'true'
    return 'false'


@app.route("/verify/<verify_key>", methods=["GET", "POST"])
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
        return ("Your account has been already verified or the link has been expired")


@app.route("/verifyoption", methods=["GET", "POST"])
def verifyoption():
    email = request.form.get("email", None)
    user = load_user(email)
    if email:
        key = random_key(10) + email[:5]
        with db.ConnectionInstance() as queries:
            queries.make_verifykey(user.user_id,key)
        send_verification(email,key)
        return render_template("verify_send.html", email=email)



##################################################################


if __name__ == '__main__':
    app.run()
