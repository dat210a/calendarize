import json, re
from flask import Blueprint, render_template, redirect, abort, request
from jinja2 import TemplateNotFound
from flask_login import login_required, current_user
from classes import db_queries as db
from classes.db_queries_friends import ConnectionInstanceFriends as friends_queries
from funcs.send_email import send_friend_request


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
    except TemplateNotFound:
        abort(404)


@sidebar.route('/friend_request', methods=['POST', 'GET'])
def friend_request():
    if request.method == 'POST':
        invites = re.sub( '\s+', ' ', request.form.get('invites', '')).strip()
        invites = re.split(',| |;', invites)
        with friends_queries() as queries:
            for email in invites:
                # send email to email
                sender = current_user.username()
                sent = send_friend_request(sender,email)
                #add request to database
                if sent and not queries.check_friend(current_user.user_id, queries.get_user_id(email), email):
                    queries.add_friend(current_user.user_id, email)
            return json.dumps({'success' : 'true'})
    return json.dumps({'success' : 'false'})


@sidebar.route('/accept_friend', methods=['POST', 'GET'])
def accept_friend():
    if request.method == 'POST':
        sender = request.form.get('friend_id', None)
        if sender:
            with friends_queries() as queries:
                if queries.check_friend(sender, None, current_user.email):
                    queries.accept_friend(sender, current_user.user_id, current_user.email)
            return json.dumps({'success' : 'true'})
    return json.dumps({'success' : 'false'})


@sidebar.route('/remove_friend', methods=['POST', 'GET'])
def remove_friend():
    if request.method == 'POST':
        friend_email = request.form.get('email', None)
        friend_id = request.form.get('friend_id', None)
        with friends_queries() as queries:
            if friend_email:
                friend_id = queries.get_user_id(friend_email)
            elif friend_id:
                friend_email = queries.get_user_email(friend_id)
            else:
                return json.dumps({'success' : 'false'})
            row = queries.check_friend(current_user.user_id, friend_id, friend_email)
            if row:
                queries.remove_friend(row)
            row = queries.check_friend(friend_id, current_user.user_id, current_user.email)
            if row:
                queries.remove_friend(row)
            return json.dumps({'success' : 'true'})
    return json.dumps({'success' : 'false'})