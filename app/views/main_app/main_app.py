import json, pytz, re
from datetime import datetime, date
from flask import Blueprint, render_template, redirect, abort, request
from flask_login import login_required, current_user
from classes import db_queries as db
from classes.db_queries_friends import ConnectionInstanceFriends as friends_queries
from funcs.send_email import send_invite
from funcs import data_verification as verify
from funcs.helpers import type_handler


mainApp = Blueprint('mainApp', __name__,
                        template_folder='templates')


@mainApp.before_request
@login_required
def before_request():
    pass


@mainApp.route('/index_user')
def index_user():
    """
    """
    with friends_queries() as queries:
        invites = queries.get_user_invites(current_user.user_id)
        invites = len(invites) if invites else 0
        invites += len(queries.get_friend_requests(current_user.email))
    return render_template('index_user.html', name=current_user.username(), notifier=invites)


@mainApp.route('/calendar')
def calendar():
    """
    """
    with friends_queries() as queries:
        invites = queries.get_user_invites(current_user.user_id)
        invites = len(invites) if invites else 0
        invites += len(queries.get_friend_requests(current_user.email))
    return render_template('calendar.html', name=current_user.username(), notifier=invites)


@mainApp.route('/get_data')
def get_data():
    """
    """
    with db.ConnectionInstance() as queries:
        calendar_ids = queries.get_calendars(current_user.user_id)
        cal_details = queries.get_calendars_details(calendar_ids)
        event_details = queries.get_events_details(calendar_ids)
    return json.dumps([cal_details, event_details], default=type_handler)


@mainApp.route('/add_calendar', methods=['POST', 'GET'])
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
                        # send email to email
                        sent = send_invite(current_user.username(),email,cal_name)
                        if sent and queries.check_invite(email, new_cal_id):
                            role = 1 # 0: owner, 1: admin, 2: contributor, 3: user
                            queries.send_invite(new_cal_id, queries.get_user_id(email), current_user.user_id, role, email)
                    cal_data = queries.get_calendars_details((new_cal_id,))[0]
                    return json.dumps({'success' : 'true', 'data' : json.dumps(cal_data, default=type_handler)})
    return json.dumps({'success' : 'false'})


@mainApp.route('/edit_calendar', methods=['POST', 'GET'])
def edit_calendar():
    cal_data = {}
    if request.method == "POST":
        cal_data['calendar_name'] = request.form.get('newCalendarName', None)
        cal_data['calendar_color'] = request.form.get('color', None)[1:]
        cid = request.form.get('cal_id', None)
        with db.ConnectionInstance() as queries:
            role = queries.get_calendar_role(current_user.user_id, cid)
            if role is not None and role <= 2:
                success = queries.update_calendar(cal_data, cid)
                if success:
                    # parse 'invites' string and send invites
                    invites = re.sub( '\s+', ' ', request.form.get('invites', '')).strip()
                    invites = re.split(',| |;', invites)
                    for email in invites:
                        # send email to email
                        sent = send_invite(current_user.username(),email,cal_data['calendar_name'])
                        if sent and queries.check_invite(email, cid):
                            role = 1 # 0: owner, 1: admin, 2: contributor, 3: user
                            queries.send_invite(cid, queries.get_user_id(email), current_user.user_id, role, email)
                    cal_data = queries.get_calendars_details((cid,))[0]
                    return json.dumps({'success' : 'true', 'data' : json.dumps(cal_data, default=type_handler)})
    return json.dumps({'success' : 'false'})


@mainApp.route('/request_calandar', methods=['POST', 'GET'])
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


@mainApp.route('/join_calander', methods=['POST', 'GET'])
def join_calander():
    if request.method == 'POST':
        id = request.form.get("calendar_id", None)
        role = request.form.get("role", None)
        with db.ConnectionInstance() as q:
            if q.check_for_invite(current_user.user_id, id, role) == True:
                q.join_calander(id, current_user.user_id, role)
                return 'true'
    return 'false'


@mainApp.route('/decline_calander', methods=['POST', 'GET'])
def decline_calander():
    if request.method == 'POST':
        id = request.form.get("calendar_id", None)
        role = request.form.get("role", None)
        with db.ConnectionInstance() as q:
            if q.check_for_invite(current_user.user_id, id, role) == True:
                return 'true'
    return 'false'


@mainApp.route('/invite_calendar', methods=['POST', 'GET'])
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


@mainApp.route('/leave_calander', methods=['POST', 'GET'])
def leave_calander():
    if request.method == 'POST':
        cid = request.form.get("calender_id", None)
        with db.ConnectionInstance() as q:
            q.leave_calander(cid, current_user.user_id)
        return 'true'
    return 'false'


@mainApp.route('/add_event', methods=['POST', 'GET'])
def add_event():
    if request.method == "POST":
        response, data = verify.prepare_new_event_data()
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


@mainApp.route('/edit_event', methods=['POST', 'GET'])
def edit_event():
    if request.method == "POST":
        eid = request.form.get('event_id', None)
        if eid is None:
            return json.dumps({'success' : 'false', 'message': 'Missing event id'})

        response, data = verify.prepare_edit_event_data()
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


@mainApp.route('/set_instance', methods=['POST', 'GET'])
def set_instance():
    if request.method == "POST":
        eid = request.form.get('event_id', None)
        year = request.form.get('year', None)
        if not eid or not year:
            return json.dumps({'success' : 'false', 'message': 'Non specified event id or year'})

        response, data = verify.prepare_set_instance_data()
        if not response:
            return json.dumps({'success' : 'false', 'message': data})

        with db.ConnectionInstance() as queries:
            cid = queries.get_event_calendar_id(eid)
            role = queries.get_calendar_role(current_user.user_id, cid)
            if role is not None and role <= 2:
                chid = queries.get_child_id(eid, year)
                if chid:
                    queries.update_child(data, chid)
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


@mainApp.route('/delete_event', methods=['POST', 'GET'])
def delete_event():
    if request.method=="POST":
        event = request.form.get('event_id', None)
        if event:
            with db.ConnectionInstance() as queries:
                cal = queries.get_event_calendar_id(event)
                role = queries.get_calendar_role(current_user.user_id, cal)
                if role is not None and role < 2:
                    queries.db_del_event(event)
                    # TODO delete files
                    return 'true'
    return 'false'


@mainApp.route('/delete_instance', methods=['POST', 'GET'])
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


@mainApp.route('/delete_calendar', methods=['POST', 'GET'])
def delete_cal():
    if request.method=="POST":
        cal = request.form.get('calendar_id', None)
        if cal:
            with db.ConnectionInstance() as queries:
                role = queries.get_calendar_role(current_user.user_id, cal)
                if role is not None and role <= 1:
                    queries.db_del_cal(cal)
                    return 'true'
    return 'false'