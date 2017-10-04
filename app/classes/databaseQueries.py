from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared


class DatabaseQueries:

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

    def get_user_id(self, username):
        self.__cur.execute("select UserID FROM user where ? = Username", username)