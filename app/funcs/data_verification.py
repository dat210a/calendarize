from flask import request
from datetime import datetime, date
from flask_login import current_user

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