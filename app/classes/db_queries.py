import logging
import hashlib
import json
import pprint as pp
from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared

conf_file = 'cfg/db.json'


with open(conf_file, 'r') as cf:
    # Loads login information from file for security
    data = json.load(cf)
    DB_USER = data['username']
    DB_PW = data['password']
    DB_DB = data['database']
    DB_HOST = data['host']


def secure_fn(fname):
    conv = fname.encode('utf-8')
    sec = hashlib.sha224(conv)
    return sec.hexdigest()


class ConnectionInstance:
    """
    PyCharm note: If you're getting linting errors, go to Settings/Preferences > Tools > Database > User Parameters,
    check the two checkboxes and add %\((\w+)\)s and %s for all languages.
    """

    def __init__(self):
        self.__con = connector.connect(user=DB_USER,
                                       password=DB_PW,
                                       host=DB_HOST,
                                       database=DB_DB)
        self.__cur = self.__con.cursor(dictionary=True, cursor_class=MySQLCursorPrepared)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__con.close()

    def db_generic_select(self, attr, table, val, cond):
        # This is just a test to see how generic a secure SQL function can be, it's not intended to be used anywhere.
        sql = "SELECT %s FROM %s WHERE %s = %s"
        self.__cur.execute(sql, [attr, table, val, cond])
        return self.__cur.fetchall()

#######################################################################################
        # Retrieval

    def get_user_id(self, email):
        sql = "SELECT user_id FROM users WHERE ? = user_email"
        self.__cur.execute(sql, [email])
        res = self.__cur.fetchone()
        return res[0]

    def get_pass_hash(self, email):
        sql = "SELECT user_password FROM users WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        res = self.__cur.fetchone()
        return res[0].decode('utf-8')

    def get_username(self, email):
        sql = "SELECT user_name FROM users WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        res = self.__cur.fetchone()
        return res[0].decode('utf-8')

    def get_calendars(self):
        sql = "SELECT calendar_id FROM calendars"
        self.__cur.execute(sql)
        return self.__cur.fetchall()

    def get_calendar_members(self, cid):
        sql = "SELECT calendar_members FROM calendars WHERE calendar_id = %s"
        self.__cur.execute(sql, [cid])
        return self.__cur.fetchall()

    def db_get_cal_admin(self, cid=None, eid=None):
        # Fetches a list of admins for a calendar
        if cid:
            sql = "SELECT calendar_admins FROM calendars WHERE calendar_id = %s"
            self.__cur.execute(sql, [cid])
        elif eid and not cid:
            sql = "SELECT calendar_admins " \
                  "FROM calendars WHERE calendar_id = (SELECT event_belongs_to FROM events WHERE event_id = %s)"
            self.__cur.execute(sql, [eid])
        else:
            return None
        payload = self.__cur.fetchall()
        logging.debug('Result of calendar admin db request: {}'.format(payload))
        return payload

#######################################################################################
        # Insertion

    def add_user(self, username, email, hashedpass):
        query = 'INSERT INTO users (user_name, user_email, user_password) VALUES (?,?,?)'
        user_data = [username, email, hashedpass]
        try:
            self.__cur.execute(query, user_data)
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert new user with data:\n{}'.format(e, pp.pformat(user_data)))
            self.__con.rollback()
            return False

    def add_event(self, event_data):
        sql = "INSERT INTO events " \
              "(event_id, event_name, event_date_created, event_details, " \
              "event_location, event_start, event_end, event_time, event_extra)" \
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.__cur.execute(
            sql,
            [
                event_data['id'],
                event_data['name'],
                event_data['created'],
                event_data['details'],
                event_data['location'],
                event_data['start'],
                event_data['end'],
                event_data['time'],
                event_data['extra']
            ]
        )
        sql = "INSERT INTO calendar_events (calendar_id, event_id) VALUES (?, ?)"
        self.__cur.execute(sql, [event_data['parent'], event_data['id']])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert event with data:\n{}'.format(e, pp.pformat(event_data)))
            self.__con.rollback()

    def add_calendar(self, cal_data):
        sql = "INSERT INTO calendars " \
              "(calendar_id, calendar_name, calendar_date_created, calendar_details, calendar_owner, calendar_extra) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        self.__cur.execute(sql, [
            cal_data['id'],
            cal_data['name'],
            cal_data['created'],
            cal_data['details'],
            cal_data['owner'],
            cal_data['extra']
        ])
        sql = "INSERT INTO user_calendars (user_id, calendar_id) VALUES (?, ?)"
        self.__cur.execute(sql, [cal_data['owner'], cal_data['id']])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert calendar with data:\n{}'.format(e, pp.pformat(cal_data)))
            self.__con.rollback()

    def fetch_data_for_display(self, uid):
        sql = "SELECT calendar_id FROM user_calendars WHERE user_id = %s"
        self.__cur.execute(sql, [uid])
        res = self.__cur.fetchall()
        cals = [r[0] for r in res]

        sql = "SELECT event_id FROM calendar_events WHERE calendar_id = ?"
        if len(cals) > 1:
            for i in range(len(cals) - 1):
                sql += " OR calendar_id = ?"
        self.__cur.execute(sql, cals)
        res = self.__cur.fetchall()
        events = [r[0] for r in res]

        sql = "SELECT * FROM events WHERE event_id = ?"
        if len(events) > 1:
            for i in range(len(events)-1):
                sql += " OR event_id = ?"
        # TODO complete with relevant values to fetch and return

#######################################################################################
            # Deletion

    def db_del_user(self, uid):
        self.__cur.execute("UPDATE user SET deleted=1 WHERE ? = UserID", [uid])
        self.__con.commit()

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE event SET deleted=1 WHERE ? = EventID", [eid])
        self.__con.commit()

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendar SET deleted=1 WHERE ? = CalendarID", [cid])
        self.__con.commit()

