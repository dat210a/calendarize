import logging
import json
import pprint as pp
from funcs.file_tools import save_file
from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared

conf_file = "app/cfg/db.json"

with open(conf_file, 'r') as cf:
    # Loads login information from file for security
    data = json.load(cf)
    DB_USER = data['username']
    DB_PW = data['password']
    DB_DB = data['database']
    DB_HOST = data['host']


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
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))
            return None

    def get_user_activity(self, email):
        sql = "SELECT active FROM users WHERE ? = user_email"
        self.__cur.execute(sql, [email])
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))
            return None

    def get_pass_hash(self, email):
        sql = "SELECT user_password FROM users WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile retrieving password hash for user with email:\n{}'.format(e, email))
            return None

    def get_username(self, email):
        sql = "SELECT user_name FROM users WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile trying to retreive username with email:\n{}'.format(e, email))
            return None

    def get_calendars(self):
        sql = "SELECT calendar_id FROM calendars"
        self.__cur.execute(sql)
        try:
            return [x[0] for x in self.__cur.fetchall()]
        except Exception as e:
            logging.debug('{}\nWhile trying to retrieve calendar IDs'.format(e))
            return None

    def get_event_files(self, eid, rec):
        sql = "SELECT file_name FROM event_files WHERE event_id = ? AND recurring = ?"
        self.__cur.execute(sql, eid, rec)
        try:
            return [x[0] for x in self.__cur.fetchall()]
        except Exception as e:
            logging.debug('{}\nWhile fetching files for event with id: {}'.format(e, eid))

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
        try:
            payload = ([x[0] for x in self.__cur.fetchall()])
            logging.debug('Result of calendar admin db request: {}'.format(payload))
            return payload
        except Exception as e:
            logging.debug('{}\nWhile trying to retrieve admins for calendar.\n'
                          'Input parameters: cid={} eid={}'.format(e, cid, eid))
            return None

    def fetch_data_for_display(self, uid):
        sql = "SELECT calendar_id FROM user_calendars WHERE user_id = %s"
        self.__cur.execute(sql, [uid])
        try:
            res = self.__cur.fetchall()
            cals = [r[0] for r in res]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, uid))
            return None

        sql = "SELECT calendar_id, calendar_name FROM calendars WHERE calendar_id = %s"
        if len(cals) > 1:
            for i in range(len(cals) - 1):
                sql += " OR calendar_id = ?"
        self.__cur.execute(sql, cals)
        try:
            calendars = self.__cur.fetchall()
            calendars2 = [dict(zip(('id', 'name'), calendar)) for calendar in calendars]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, uid))
            return None

        sql = "SELECT event_id, event_name, event_calendar_id, event_start, event_end, event_recurring FROM events WHERE event_calendar_id = ?"
        if len(cals) > 1:
            for i in range(len(cals) - 1):
                sql += " OR event_calendar_id = ?"
        self.__cur.execute(sql, cals)
        try:
            events = self.__cur.fetchall()
            events2 = [dict(zip(('id', 'name', 'group', 'start_date', 'end_date', 'recurring'), event)) for event in events]
            return [calendars2, events2]
        except Exception as e:
            logging.debug('{}\nWhile fetching events for calendar(s): {}'.format(e, cals))
            return None

    def get_resetkey(self, uid):
        # DELETE FROM forgot WHERE expires < NOW()
        pass

    def get_last_ID(self):
        sql = 'SELECT LAST_INSERT_ID();'
        self.__cur.execute(sql)
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile retrieving ID for the last INSERT'.format(e))
            return None

#######################################################################################
        # Insertion

    def add_user(self, username, email, hashedpass):
        query = 'INSERT INTO users (user_name, user_email, user_password) VALUES (?,?,?);'
        user_data = [username, email, hashedpass]
        try:
            self.__cur.execute(query, user_data)
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nWhile trying to insert user with data:\n'
                          '\tUsername: {}\n'
                          '\tEmail: {}\n'
                          '\tPW hash: {}'.format(e, username, email, hashedpass))
            self.__con.rollback()
            return None
        
    def add_calendar(self, created, owner, cal_name="Default"):
        sql = "INSERT INTO calendars " \
              "(calendar_name, calendar_date_created, calendar_owner) " \
              "VALUES (?, ?, ?)"
        self.__cur.execute(sql, [
            cal_name,
            created,
            owner,
        ])
        calendar_id = self.get_last_ID()
        sql = "INSERT INTO user_calendars (user_id, calendar_id, role) VALUES (?, ?, ?)"
        self.__cur.execute(sql, [owner, calendar_id, 0])
        try:
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert calendar with data:\n{}'.format(e, pp.pformat(cal_name)))
            self.__con.rollback()
            return None

    def add_event(self, event_data, created, owner):
        sql = "INSERT INTO events " \
              "(event_name, event_calendar_id, event_date_created, event_owner, event_start, event_end, event_recurring)" \
              "VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.__cur.execute(
            sql,
            [
                event_data['newEventName'],
                event_data['calendarID'],
                created,
                owner,
                event_data['startDate'],
                event_data['startDate'] if event_data['endDate'] == '' else event_data['endDate'],
                1 if 'recurring' in event_data else 0,
            ]
        )
        try:
            self.__con.commit()
            if 'file' in event_data.keys():
                self.add_file(event_data['file'], event_data['id'])
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert event with data:\n{}'.format(e, pp.pformat(event_data)))
            self.__con.rollback()
            return None

    def add_file(self, rqdat, eid, rec=0):
        fname = save_file(rqdat, eid)
        if fname:
            sql = "INSERT INTO event_files (event_id, file_name, recurring) VALUES (?, ?, ?)"
            self.__cur.execute(sql, eid, fname, rec)
            try:
                self.__con.commit()
            except Exception as e:
                logging.debug('{}\nWhile adding file with name:\n{}'.format(e, fname))
                self.__con.rollback()
        else:
            pass  # Does nothing if there is no file

    def make_resetkey(self, uid, resetkey):
        # INSERT INTO forgot (resetkey, expires) VALUES (whatever, NOW() + INTERVAL 48 HOUR)
        pass


#######################################################################################
            # Update

    def activate_user(self, email):
        sql = 'UPDATE users SET active = 1 WHERE ? = user_email;'
        self.__cur.execute(sql, [email])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))


    def update_user(self, user_data):
        #TODO
        pass

    def update_calendar(self, calendar_data):
        #TODO
        pass
    
    def update_event(self, event_data):
        #TODO
        pass

    def update_role(self, data):
        #TODO
        pass


#######################################################################################
            # Deletion

    def db_del_user(self, uid):
        self.__cur.execute("UPDATE user SET deleted=1 WHERE ? = UserID", [uid])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile trying to delete user: {}'.format(e, uid))
            self.__con.rollback()

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE event SET deleted=1 WHERE ? = EventID", [eid])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile trying to delete event: {}'.format(e, eid))
            self.__con.rollback()

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendar SET deleted=1 WHERE ? = CalendarID", [cid])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile trying to delete calendar: {}'.format(e, cid))
            self.__con.rollback()
