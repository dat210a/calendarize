import logging
import json
import pprint as pp
from funcs.file_tools import save_file
from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared

conf_file = "cfg/db.json"

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
        sql = "SELECT user_id FROM users WHERE ? = user_email "
        self.__cur.execute(sql, [email])
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))
            return None

    def get_validation_info(self, calendar_id, user_id):
        sql = "SELECT role FROM user_calendars WHERE calendar_id = ? AND user_id = ?"
        self.__cur.execute(sql, [calendar_id, user_id])
        return self.__cur.fetchone()[0]

    def get_user_activity(self, email):
        sql = "SELECT active FROM users WHERE ? = user_email"
        self.__cur.execute(sql, [email])
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))
            return None

    def join_calander(self, calender_id, user_id, role):
        self.__cur.execute("SELECT unique_id from user_calendars ORDER BY unique_id DESC LIMIT 1")
        unique_id = self.__cur.fetchone()
        if unique_id[0] == None:
            unique_id = 1
        else:
            unique_id = unique_id[0] + 1
        sql = "INSERT INTO user_calendars VALUES (?, ?, ?, ?)"
        self.__cur.execute(sql, [user_id, calender_id, role, unique_id])
        self.__con.commit()


    def leave_calander(self, calender_id, user_id):
        sql = "DELETE FROM user_calendars WHERE user_id = ? and calendar_id = ?"
        self.__cur.execute(sql, [user_id, calender_id])
        self.__con.commit()

    def send_invite(self, calender_id, user_id, sender_id, role):
        sql = "INSERT INTO calendar_invites VALUES (?,?,?,?,?)"
        self.__cur.execute("SELECT unique_id from calendar_invites ORDER BY unique_id DESC LIMIT 1")
        unique_id = self.__cur.fetchone()
        if unique_id == None:
            unique_id = 1
        else:
            unique_id = unique_id[0] + 1
        self.__cur.execute(sql, [unique_id, calender_id, user_id, sender_id, role])
        self.__con.commit()

    def get_pass_hash(self, email):
        sql = "SELECT user_password FROM users WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile retrieving password hash for user with email:\n{}'.format(e, email))
            return None

    # def get_username(self, email):
    #     sql = "SELECT user_name FROM users WHERE user_email = ?"
    #     self.__cur.execute(sql, [email])
    #     try:
    #         res = self.__cur.fetchone()
    #         return res[0].decode('utf-8')
    #     except Exception as e:
    #         logging.debug('{}\nWhile trying to retreive username with email:\n{}'.format(e, email))
    #         return None

    def get_calendars(self, uid):
        sql = "SELECT calendar_id FROM user_calendars WHERE user_id = ?"
        self.__cur.execute(sql, [uid])
        try:
            res = self.__cur.fetchall()
            return [r[0] for r in res]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, uid))
            return None

    def get_event_calendar_id(self, eid):
        sql = "SELECT event_calendar_id FROM events WHERE event_id = ?"
        self.__cur.execute(sql, [eid])
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile fetching parent calendar for event: {}'.format(e, eid))
            return None   

    def get_calendar_role(self, uid, cid):
        sql = "SELECT role FROM user_calendars WHERE user_id = ? AND calendar_id = ?"
        self.__cur.execute(sql, [uid, cid])
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, uid))
            return None

    def get_event_files(self, eid, rec):
        sql = "SELECT file_name FROM event_files WHERE event_id = ? AND recurring = ?"
        self.__cur.execute(sql, eid, rec)
        try:
            return [x[0] for x in self.__cur.fetchall()]
        except Exception as e:
            logging.debug('{}\nWhile fetching files for event with id: {}'.format(e, eid))

    # def db_get_cal_admin(self, cid=None, eid=None):
    #     # Fetches a list of admins for a calendar
    #     if cid:
    #         sql = "SELECT calendar_admins FROM calendars WHERE calendar_id = %s"
    #         self.__cur.execute(sql, [cid])
    #     elif eid and not cid:
    #         sql = "SELECT calendar_admins " \
    #               "FROM calendars WHERE calendar_id = (SELECT event_belongs_to FROM events WHERE event_id = %s)"
    #         self.__cur.execute(sql, [eid])
    #     else:
    #         return None
    #     try:
    #         payload = ([x[0] for x in self.__cur.fetchall()])
    #         logging.debug('Result of calendar admin db request: {}'.format(payload))
    #         return payload
    #     except Exception as e:
    #         logging.debug('{}\nWhile trying to retrieve admins for calendar.\n'
    #                       'Input parameters: cid={} eid={}'.format(e, cid, eid))
    #         return None

    def fetch_data_for_display(self, uid):
        cals = self.get_calendars(uid)

        sql = "SELECT calendar_id, calendar_name FROM calendars " \
              "WHERE calendar_id IN(" + ",".join("?"*len(cals)) + ") " \
              "AND deleted = 0"
        self.__cur.execute(sql, cals)
        try:
            calendars = self.__cur.fetchall()
            calendars2 = [dict(zip(('id', 'name'), calendar)) for calendar in calendars]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, uid))
            return None

        sql = "SELECT event_id, event_name, event_calendar_id, event_start, event_end, event_recurring FROM events " \
              "WHERE event_calendar_id IN(" + ",".join("?"*len(cals)) + ") " \
              "AND deleted = 0"
        self.__cur.execute(sql, cals)
        try:
            events = self.__cur.fetchall()
            events2 = [dict(zip(('id', 'name', 'group', 'start_date', 'end_date', 'recurring'), event)) for event in events]
            return [calendars2, events2]
        except Exception as e:
            logging.debug('{}\nWhile fetching events for calendar(s): {}'.format(e, cals))
            return None

    def get_reset_info(self, resetkey):
        sql ="SELECT user_email FROM users WHERE resetkey=? and expires > now()"
        self.__cur.execute(sql, [resetkey])
        try:
            res = self.__cur.fetchone()
            return res[0].decode("utf-8")
        except Exception as e:
            logging.debug('{}\nWhile checking resetkey and expire:\n{}'.format(e, resetkey))
            return None

    def get_verify_info(self, verify_key):
        sql ="SELECT user_email FROM users WHERE verify_key=? and expires > now()"
        self.__cur.execute(sql, [verify_key])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile checking resetkey and expire:\n{}'.format(e, verify_key))
            return None

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

    def add_user(self, created, email, hashedpass,verify_key):
        query = 'INSERT INTO users (user_date_created, user_email, user_password,verify_key,expires) VALUES (?,?,?,?, now()+ INTERVAL 24 HOUR);'
        user_data = [created, email, hashedpass, verify_key]
        self.__cur.execute(query, user_data)
        try:
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nWhile trying to insert user with data:\n'
                          '\tEmail: {}\n'
                          '\tPW hash: {}'.format(e, email, hashedpass))
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
                event_data['endDate'],
                1 if 'recurring' in event_data else 0,
            ]
        )
        try:
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert event with data:\n{}'.format(e, pp.pformat(event_data)))
            self.__con.rollback()
            return None

    def add_file(self, rqdat, eid):
        fname = save_file(rqdat, eid)
        if fname:
            sql = "INSERT INTO event_files (event_id, file_name) VALUES (?, ?)"
            self.__cur.execute(sql, eid, fname)
            try:
                self.__con.commit()
            except Exception as e:
                logging.debug('{}\nWhile adding file with name:\n{}'.format(e, fname))
                self.__con.rollback()
        else:
            pass  # Does nothing if there is no file


#######################################################################################
            # Update

    def make_resetkey(self, email, resetkey):
        sql ="UPDATE users SET resetkey=?,expires= NOW() + INTERVAL 48 HOUR WHERE user_email=?"
        self.__cur.execute(sql, (resetkey,email))
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile setting resetkey for email:\n{}'.format(e, email))
            self.__con.rollback()

    def set_new_password(self, email, new_password):
        sql = "UPDATE users SET user_password =?, resetkey='' WHERE user_email = ?"
        self.__cur.execute(sql, (new_password,email))
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile setting user new password:\n{}'.format(e, email))
            self.__con.rollback()

    def activate_user(self, email):
        sql = "UPDATE users SET active = 1, verify_key='' WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))
            self.__con.rollback()

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
        self.__cur.execute("UPDATE users SET deleted = 1 WHERE ? = user_id", [uid])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile trying to delete user: {}'.format(e, uid))
            self.__con.rollback()

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE events SET deleted=1 WHERE ? = event_id", [eid])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile trying to delete event: {}'.format(e, eid))
            self.__con.rollback()

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendars SET deleted=1 WHERE ? = calendar_id", [cid])
        try:
            self.__con.commit()
        except Exception as e:
            logging.debug('{}\nWhile trying to delete calendar: {}'.format(e, cid))
            self.__con.rollback()
