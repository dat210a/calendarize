from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from classes import db_queries as db

sidebar = Blueprint('sidebar', __name__,
                        template_folder='templates')


@sidebar.before_request
@login_required
def before_request():
    pass


@sidebar.route('/notifications')
def notifications():
    with db.ConnectionInstance() as q:
        invites = q.get_user_invites(current_user.user_id)
        return render_template('notifications.html', notifications=invites)


@sidebar.route('/display_profile')
def profile():
    with db.ConnectionInstance() as q:
        phone = q.get_user_data(current_user.user_id)
        name = current_user.username()
        user_data = {"name": name, "email": current_user.email, "phone": phone}
    return render_template('display_profile.html', name=name, email=current_user.email, phone=phone)


# @sidebar.route('/display_event')
# def event(eid):
#     with db.ConnectionInstance() as q:
#         details = q.get_events_details()
#     return render_template('display_event.html', event=details)


@sidebar.route('/<path>')
def load_sidebar(path):
    return render_template(path + '.html')