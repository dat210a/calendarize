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
import logging, json
from datetime import datetime, date
from classes import db_queries as db
from flask import Flask, flash, render_template, session, g, request, url_for, redirect
from classes.user import User
from flask_login import login_required, fresh_login_required, logout_user, login_user, current_user
from funcs.logIn import check_password, hash_password, init_login, user_exists, load_user
from funcs.file_tools import load_file, load_profile_pic
from funcs.send_email import init_mail, send_verification, random_key
from views.sidebar import sidebar
from views.main_app import main_app
from views.verify_and_recover import verify_and_recover

# app initialization
app = Flask(__name__)
app.register_blueprint(sidebar.sidebar, url_prefix='/side')
app.register_blueprint(main_app.mainApp)
app.register_blueprint(verify_and_recover.verifyAndRecover)

# config setup
app.config['DEBUG'] = False

# needed for session cookies
app.secret_key = 'hella secret'

# initialize login and mail modules
init_login(app)
init_mail(app)


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


@app.route('/')
def index():
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
    return render_template('index.html')


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
                key = random_key(10) + email
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
    # TODO redirect to: you have successfully logged out
    return redirect('/')


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


@app.route('/images/<folder>/<filename>')
def profile_picture(folder, filename):
    return load_profile_pic(folder, filename)



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



##################################################################


if __name__ == '__main__':
    app.run()
