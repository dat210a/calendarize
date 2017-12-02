from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required, current_user
from classes import db_queries as db
from classes.db_queries_friends import ConnectionInstanceFriends as friends_queries


sidebar = Blueprint('sidebar', __name__,
                        template_folder='templates')


@sidebar.before_request
@login_required
def before_request():
    pass


@sidebar.route('/display_profile')
def profile():
    with db.ConnectionInstance() as q:
        phone = q.get_user_data(current_user.user_id)
        name = current_user.username()
        user_data = {"name": name, "email": current_user.email, "phone": phone}
    return render_template('display_profile.html', name=name, email=current_user.email, phone=phone)


@sidebar.route('/notifications')
def notifications():
    with db.ConnectionInstance() as q:
        invites = q.get_user_invites(current_user.user_id)
    with friends_queries() as q:
        friend_ids = q.get_friend_requests(current_user.email)
        friend_requests = [{'user_id': fid[0], 'sender': q.get_user_repr(fid[0])} for fid in friend_ids]
    return render_template('notifications.html', cal_invites=invites, friend_requests=friend_requests)


@sidebar.route('/friends')
def friends():
    with friends_queries() as q:
        friends_list = q.get_friends(current_user.user_id)
        friends = []
        pending = []
        for row in friends_list:
            if row[0] == current_user.user_id:
                if row[2]:
                    pending.append(row[2].decode('utf-8'))
                else:
                    friends.append({'name' : q.get_user_repr(row[1]), 'email' : q.get_user_email(row[1]), 'profile_pic' : '1.jpg', 'back_pic' : '1-01.jpg'})
            else:
                friends.append({'name' : q.get_user_repr(row[0]), 'email' : q.get_user_email(row[0]), 'profile_pic' : '1.jpg', 'back_pic' : '1-01.jpg'})
        return render_template('friends.html', friends=friends, pending=pending)


# @sidebar.route('/display_event')
# def event(eid):
#     with db.ConnectionInstance() as q:
#         details = q.get_events_details()
#     return render_template('display_event.html', event=details)

# temporary conveniance function until all routes are sorted
@sidebar.route('/<path>')
def load_sidebar(path):
    try:
        return render_template(path + '.html')
    except:
        abort(404)