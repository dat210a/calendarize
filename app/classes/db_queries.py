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


    def get_user_invites(self, uid):
        sql = "SELECT sender_user_id, calendar_id, role FROM calendar_invites WHERE invited_user_id = ?"
        self.__cur.execute(sql, (uid,))
        try:
            res = self.__cur.fetchall()
            roles = []
            for role in res:
                role = list(role)
                role[0] = self.get_user_repr(role[0])
                calendar_name = self.get_calendar_name(role[1])
                roles.append(role + [calendar_name])
            return [dict(zip(('sender', 'calendar_id', 'role', 'calendar_name'), role)) for role in roles]
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, uid))
            return None


    def get_calendar_name(self, cid):
        sql = "SELECT calendar_name FROM calendars WHERE ? = calendar_id "
        self.__cur.execute(sql, [cid])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile retrieving calendar name:\n{}'.format(e, cid))
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


    def send_invite(self, calender_id, user_id, sender_id, role, email):
        sql = "INSERT INTO calendar_invites VALUES (?,?,?,?,?,?)"
        self.__cur.execute("SELECT unique_id from calendar_invites ORDER BY unique_id DESC LIMIT 1")
        unique_id = self.__cur.fetchone()
        if unique_id == None:
            unique_id = 1
        else:
            unique_id = unique_id[0] + 1
        self.__cur.execute(sql, [unique_id, calender_id, user_id, email, sender_id, role])
        self.__con.commit()


    def check_invite(self, email, calendar_id):
        sql_invite = "SELECT * from calendar_invites where email = ? and calendar_id = ?"
        self.__cur.execute(sql_invite, [email, calendar_id])
        invite = self.__cur.fetchone()
        sql_invite = "SELECT * from user_calendars where user_id = ? and calendar_id = ?"
        self.__cur.execute(sql_invite, [self.get_user_id(email), calendar_id])
        calendar = self.__cur.fetchone()
        if calendar == None and invite == None:
            return True
        return False


    def check_for_invite(self, user_id, calendar_id, role):
        sql = "SELECT invited_user_id, calendar_id, role, unique_id FROM calendar_invites WHERE invited_user_id = ? AND calendar_id = ?"
        self.__cur.execute(sql, [user_id, calendar_id])
        res = self.__cur.fetchone()
        if res == None:
            return False
        if (res[0] == user_id) and (res[1] == int(calendar_id)) and (res[2] == int(role)):
            self.remove_invite(int(res[3]))
            return True
        return False

    def remove_invite(self, unique_id):
        sql = "DELETE FROM calendar_invites WHERE unique_id = ?"
        self.__cur.execute(sql, [unique_id])
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

    def get_user_name(self, uid):
        sql = "SELECT user_name FROM users WHERE user_id = ?"
        self.__cur.execute(sql, [uid])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile trying to retreive username with email:\n{}'.format(e, uid))
            return None

    def get_user_email(self, uid):
        sql = "SELECT user_email FROM users WHERE user_id = ?"
        self.__cur.execute(sql, [uid])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile trying to retreive username with email:\n{}'.format(e, uid))
            return None

    def get_user_repr(self, id):
        name = self.get_user_name(id)
        if not name:
            return self.get_user_email(id)
        return name

    def get_user_data(self, uid):
        user_data = ['user_phone']
        sql = "SELECT (" + ",".join(user_data) + ") FROM users WHERE user_id = ?"
        self.__cur.execute(sql, [uid])
        try:
            res = self.__cur.fetchone()
            return res[0].decode('utf-8')
        except Exception as e:
            logging.debug('{}\nWhile trying to retreive user data with id:\n{}'.format(e, uid))
            return None

    def get_calendars(self, uid):
        sql = "SELECT calendar_id FROM user_calendars WHERE user_id = ?"
        self.__cur.execute(sql, [uid])
        try:
            res = self.__cur.fetchall()
            return [r[0] for r in res]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, uid))
            return []

    def get_calendar_users(self, cid):
        sql = "SELECT user_id FROM user_calendars WHERE calendar_id = ?"
        self.__cur.execute(sql, [cid])
        try:
            res = self.__cur.fetchall()
            return [r[0] for r in res]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, cid))
            return []

    def get_calendar_pending(self, cid):
        sql = "SELECT email FROM calendar_invites WHERE calendar_id = ?"
        self.__cur.execute(sql, [cid])
        try:
            res = self.__cur.fetchall()
            return [r[0] for r in res]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendars for user: {}'.format(e, cid))
            return []

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

    def get_calendar_name(self, calender_id):
        sql = "SELECT calendar_name FROM calendars WHERE calendar_id = ?"
        self.__cur.execute(sql, [calender_id])
        try:
            res = self.__cur.fetchone()
            return res[0].decode("utf-8")
        except Exception as e:
            logging.debug('{}\nWhile fetching calendar name: {}'.format(e, uid))
            return None

    def get_calendars_details(self, cids):
        if len(cids) == 0:
            return None
        cal_keys = ["calendar_id", "calendar_name", "calendar_color", "calendar_owner_id"]
        sql = "SELECT " + ",".join(cal_keys) + " FROM calendars " \
              "WHERE calendar_id IN(" + ",".join("?"*len(cids)) + ") " \
              "AND deleted = 0"
        self.__cur.execute(sql, cids)
        try:
            calendars = []
            for calendar in self.__cur.fetchall():
                calendar = list(calendar)
                member_ids = self.get_calendar_users(calendar[0])
                members = []
                for member in member_ids:
                    members.append(self.get_user_repr(member))
                pending = self.get_calendar_pending(calendar[0])
                calendar[3] = self.get_user_repr(calendar[3])
                calendars.append(calendar+[members]+[pending])
            return [dict(zip(cal_keys+['members']+['pending'], calendar)) for calendar in calendars]
        except Exception as e:
            logging.debug('{}\nWhile fetching calendar(s) details for user: {}'.format(e, cids))
            return None


    def get_events_details(self, cids):
        if len(cids) == 0:
            return None
        data_key = ["event_id", "event_owner_id", "event_calendar_id", "event_name", "event_start", "event_end", "event_recurring", "event_fixed_date", "event_details"]
        sql = "SELECT " + ",".join(data_key) + " FROM events " \
              "WHERE event_calendar_id IN(" + ",".join("?"*len(cids)) + ") " \
              "AND deleted = 0"
        self.__cur.execute(sql, cids)
        try:
            events = []
            for event in self.__cur.fetchall():
                event = list(event)
                files = self.get_event_files(event[0])
                children = self.get_event_children(event[0])
                event[1] = self.get_user_repr(event[1])
                events.append(event+[children]+[files])
            return [dict(zip(data_key+['children']+['files'], e)) for e in events]
        except Exception as e:
            logging.debug('{}\nWhile fetching event(s) details for calendar(s): {}'.format(e, cids))
            return None


    def get_event_files(self, eid):
        sql = "SELECT file_name FROM event_files WHERE event_id = ?"
        self.__cur.execute(sql, (eid,))
        try:
            return self.__cur.fetchall()
        except Exception as e:
            logging.debug('{}\nWhile fetching files for event with id: {}'.format(e, eid))
            return None

    def get_child_files(self, chid):
        sql = "SELECT file_name FROM child_files WHERE child_id = ?"
        self.__cur.execute(sql, (chid,))
        try:
            return self.__cur.fetchall()
        except Exception as e:
            logging.debug('{}\nWhile fetching files for child event with id: {}'.format(e, chid))
            return None

    def get_child_id(self, eid, year):
        sql = "SELECT child_id FROM event_children WHERE child_parent_id = ? AND child_year = ?"
        self.__cur.execute(sql, (eid, year))
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile fetching event child for event with id: {}'.format(e, eid))
            return None

    def get_event_children(self, eid):
        data_key = ["child_id", "child_owner_id", "child_year", "child_start", "child_end", "child_fixed_date", "child_location", "child_details", "skip_year"]
        sql = "SELECT " + ",".join(data_key) + " FROM event_children " \
              "WHERE child_parent_id = ? " \
              "AND deleted = 0"
        self.__cur.execute(sql, (eid,))
        try:
            children = []
            for child in self.__cur.fetchall():
                child = list(child)
                files = self.get_child_files(child[0])
                children.append(child+[files])
            return [dict(zip(data_key+['files'], c)) for c in children]
        except Exception as e:
            logging.debug('{}\nWhile fetching event children for event with id: {}'.format(e, eid))
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

    def add_user(self, created, email, hashedpass, verify_key):
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

    def add_calendar(self, created, owner, cal_name="Default", cal_color="f57c00"):
        sql = "INSERT INTO calendars " \
              "(calendar_name, calendar_date_created, calendar_owner_id, calendar_color) " \
              "VALUES (?, ?, ?, ?)"
        self.__cur.execute(sql, [
            cal_name,
            created,
            owner,
            cal_color
        ])
        calendar_id = self.get_last_ID()
        sql = "INSERT INTO user_calendars (user_id, calendar_id, role) VALUES (?, ?, ?)"
        self.__cur.execute(sql, [owner, calendar_id, 0])
        try:
            self.__con.commit()
            return calendar_id
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert calendar with data:\n{}'.format(e, pp.pformat(cal_name)))
            self.__con.rollback()
            return None

    def add_event(self, event_data):
        data_key = list(event_data.keys())
        sql = "INSERT INTO events " \
              "(" + ",".join(data_key) + ") " \
              "VALUES (" + ",".join("?"*len(data_key)) + ")"
        self.__cur.execute(sql, list(event_data.values()))
        try:
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert new event with data:\n{}'.format(e, pp.pformat(event_data)))
            self.__con.rollback()
            return None

    def add_child(self, child_data):
        data_key = list(child_data.keys())
        sql = "INSERT INTO event_children " \
              "(" + ",".join(data_key) + ") " \
              "VALUES (" + ",".join("?"*len(data_key)) + ")"
        self.__cur.execute(sql, list(child_data.values()))
        try:
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nOccurred while trying to insert new child event with data:\n{}'.format(e, pp.pformat(child_data)))
            self.__con.rollback()
            return None

    def add_event_file(self, rqdat, eid):
        fname = save_file(rqdat, eid)
        if fname:
            sql = "INSERT INTO event_files (event_id, file_name) VALUES (?, ?)"
            self.__cur.execute(sql, (eid, fname))
            try:
                self.__con.commit()
                return True
            except Exception as e:
                logging.debug('{}\nWhile adding file with name:\n{}'.format(e, fname))
                self.__con.rollback()
        return False

    def add_child_file(self, rqdat, eid, chid):
        fname = save_file(rqdat, eid, chid)
        if fname:
            sql = "INSERT INTO child_files (child_id, file_name) VALUES (?, ?)"
            self.__cur.execute(sql, (chid, fname))
            try:
                self.__con.commit()
                return True
            except Exception as e:
                logging.debug('{}\nWhile adding file with name:\n{}'.format(e, fname))
                self.__con.rollback()
        return False

#######################################################################################
            # Update

    def make_verifykey(self, user_id, verify_key):
        sql ="UPDATE users SET verify_key=?,expires= NOW() + INTERVAL 48 HOUR WHERE user_id=?"
        self.__cur.execute(sql, (verify_key,user_id))
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile setting new verify key:\n{}'.format(e, email))
            self.__con.rollback()
            return False

    def make_resetkey(self, email, resetkey):
        sql ="UPDATE users SET resetkey=?,expires= NOW() + INTERVAL 48 HOUR WHERE user_email=?"
        self.__cur.execute(sql, (resetkey,email))
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile setting resetkey for email:\n{}'.format(e, email))
            self.__con.rollback()
            return False

    def set_new_password(self, email, new_password):
        sql = "UPDATE users SET user_password =?, resetkey='' WHERE user_email = ?"
        self.__cur.execute(sql, (new_password,email))
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile setting user new password:\n{}'.format(e, email))
            self.__con.rollback()
            return False

    def activate_user(self, email):
        sql = "UPDATE users SET active = 1, verify_key='' WHERE user_email = ?"
        self.__cur.execute(sql, [email])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile retrieving id for email:\n{}'.format(e, email))
            self.__con.rollback()
            return False

    def update_user(self, uid, name, phone):
        sql = "UPDATE users SET user_name = ?, user_phone=? WHERE user_id = ?"
        self.__cur.execute(sql, (name, phone, uid))
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile updating user with id:\n{}'.format(e, uid))
            self.__con.rollback()
            return False

    def update_calendar(self, calendar_data):
        #TODO
        pass

    def update_event(self, event_data, eid):
        data_key = list(event_data.keys())
        sql = "UPDATE events SET "\
              + " = ?, ".join(data_key) + " = ? "\
              "WHERE event_id = ?"
        self.__cur.execute(sql, list(event_data.values()) + [eid])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile updating event with data:\n{}'.format(e,  pp.pformat(event_data)))
            self.__con.rollback()
            return False

    def update_child(self, child_data, chid):
        data_key = list(child_data.keys())
        sql = "UPDATE event_children SET "\
              + " = ?, ".join(data_key) + " = ? "\
              "WHERE child_id = ?"
        self.__cur.execute(sql, list(child_data.values()) + [chid])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile updating child event with data:\n{}'.format(e,  pp.pformat(child_data)))
            self.__con.rollback()
            return False

    def update_role(self, data):
        #TODO
        pass


#######################################################################################
            # Deletion

    def db_del_user(self, uid):
        self.__cur.execute("UPDATE users SET deleted=1, user_date_deleted = NOW() + INTERVAL 6 MONTH WHERE ? = user_id", [uid])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile trying to delete user: {}'.format(e, uid))
            self.__con.rollback()
            return False

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendars SET deleted=1, calendar_date_deleted = NOW() + INTERVAL 1 MONTH WHERE ? = calendar_id", [cid])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile trying to delete calendar: {}'.format(e, cid))
            self.__con.rollback()
            return False

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE events SET deleted=1, event_date_deleted = NOW() + INTERVAL 1 MONTH WHERE ? = event_id", [eid])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile trying to delete event: {}'.format(e, eid))
            self.__con.rollback()
            return False

    def db_del_child(self, eid, year):
        self.__cur.execute("UPDATE events SET deleted=1, child_date_deleted = NOW() + INTERVAL 1 MONTH WHERE child_parent_id = ? AND child_year = ?", [eid, year])
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile trying to delete child of event: {}'.format(e, eid))
            self.__con.rollback()
            return False
