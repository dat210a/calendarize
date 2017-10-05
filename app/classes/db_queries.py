import logging
from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared


class ConnectionInstance:
    """
    PyCharm note: If you're getting linting errors, go to Settings/Preferences > Tools > Database > User Parameters,
    check the two checkboxes and add %\((\w+)\)s and %s for all languages.
    """

    __cur = None
    __con = None

    def __init__(self, app, shard):
        self.__app = app
        self.__shard = shard
        self.__con = connector.connect(user=self.__app.config['DATABASE_USER'],
                                       password=self.__app.config['DATABASE_PASSWORD'],
                                       host=self.__app.config['DATABASE_HOST'],
                                       database=self.__app.config['DATABASE_DB'])
        self.__cur = self.__con.cursor(dictionary=True, cursor_class=MySQLCursorPrepared)
        logging.INFO('Database connection with shard {} created.'.format(self.__shard))

    def __enter__(self):
        return self.__cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__con.close()

    def db_generic_select(self, attr, table, val, cond):
        sql = "SELECT %s FROM %s WHERE %s = %s"
        res = self.__cur.execute(sql, (attr, table, val, cond))
        return res.fetchall()

    def get_user_id(self, username):
        uid = self.__cur.execute("SELECT user_id FROM user WHERE ? = user_name", username)
        return uid.fetchall()

    def db_get_cal_admin(self, cid=None, eid=None):
        # Fetches a list of admins for a calendar
        if cid:
            sql = "SELECT calendar_admins FROM calendars WHERE calendar_id = %s"
            res = self.__cur(sql, cid)
        elif eid and not cid:
            sql = "SELECT calendar_admins " \
                  "FROM calendars WHERE calendar_id = (SELECT event_belongs_to FROM events WHERE event_id = %s)"
            res = self.__cur(sql, eid)
        else:
            return None
        payload = [x for x in res.fetchall()]
        return payload

    def db_del_user(self, uid):
        self.__cur.execute("UPDATE user SET deleted=1 WHERE ? = UserID", uid)

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE event SET deleted=1 WHERE ? = EventID", eid)

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendar SET deleted=1 WHERE ? = CalendarID", cid)

