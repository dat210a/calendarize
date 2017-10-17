import logging
import hashlib
from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared


def secure_fn(fname):
    conv = fname.encode('utf-8')
    sec = hashlib.sha224(conv)
    return sec.hexdigest()


class ConnectionInstance:
    """
    PyCharm note: If you're getting linting errors, go to Settings/Preferences > Tools > Database > User Parameters,
    check the two checkboxes and add %\((\w+)\)s and %s for all languages.
    """

    def __init__(self, app):
        self.__app = app
        self.__shard = len(app.config['shards']) + 1
        self.__app.config['shards'].append(self)
        self.__con = connector.connect(user=self.__app.config['DATABASE_USER'],
                                       password=self.__app.config['DATABASE_PASSWORD'],
                                       host=self.__app.config['DATABASE_HOST'],
                                       database=self.__app.config['DATABASE_DB'])
        self.__cur = self.__con.cursor(dictionary=True, cursor_class=MySQLCursorPrepared)

        logging.INFO('Database connection with shard {} created.'.format(self.__shard))

    def __enter__(self):
        return self.__cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__app.config['shards'].remove(self)
        self.__con.close()
        logging.INFO('Database connection closed, shard {}.'.format(self.__shard))

    def db_generic_select(self, attr, table, val, cond):
        sql = "SELECT %s FROM %s WHERE %s = %s"
        self.__cur.execute(sql, [attr, table, val, cond])
        return self.__cur.fetchall()

    def get_user_id(self, username):
        self.__cur.execute("SELECT user_id FROM user WHERE ? = user_name", [username])
        return self.__cur.fetchall()

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
        logging.DEBUG('Result of calendar admin db request: {}'.format(payload))
        return payload

    def db_del_user(self, uid):
        self.__cur.execute("UPDATE user SET deleted=1 WHERE ? = UserID", [uid])
        self.__con.commit()

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE event SET deleted=1 WHERE ? = EventID", [eid])

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendar SET deleted=1 WHERE ? = CalendarID", [cid])
