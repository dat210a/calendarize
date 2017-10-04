from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared


class DatabaseQueries:
    """
    PyCharm note: If you're getting errors, go to Settings/Preferences > Tools > Database > User Parameters,
    check the two checkboxes and add %\((\w+)\)s and %s for all languages.
    """

    __cur = None
    __con = None

    def __init__(self, app):
        self.__app = app
        self.__con = connector.connect(user=self.__app.config['DATABASE_USER'],
                                       password=self.__app.config['DATABASE_PASSWORD'],
                                       host=self.__app.config['DATABASE_HOST'],
                                       database=self.__app.config['DATABASE_DB'])
        self.__cur = self.__con.cursor(dictionary=True, cursor_class=MySQLCursorPrepared)

    def __enter__(self):
        return self.__cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__con.close()

    def db_generic_select(self, attr, table, val, cond):
        sql = "SELECT %s FROM %s WHERE %s = %s"
        res = self.__cur.execute(sql, (attr, table, val, cond))
        return res

    def get_user_id(self, username):
        uid = self.__cur.execute("SELECT UserID FROM user WHERE ? = Username", username)
        return uid

    def db_del_user(self, uid):
        self.__cur.execute("UPDATE user SET deleted=1 WHERE ? = UserID", uid)

    def db_del_event(self, eid):
        self.__cur.execute("UPDATE event SET deleted=1 WHERE ? = EventID", eid)

    def db_del_cal(self, cid):
        self.__cur.execute("UPDATE calendar SET deleted=1 WHERE ? = CalendarID", cid)

