from mysql import connector
from mysql.connector.cursor import MySQLCursorPrepared

class DatabaseQueries:

    __cur = None
    __con = None

    def __init__(self):
        self.con = connector.connect(user="root", password="amysql1994J!", host="127.0.0.1", database="sys")
        self.cur = self.con.cursor(dictionary=True, cursor_class=MySQLCursorPrepared)


    def __enter__(self):
        return self.__cur


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__con.close()

    def getUserId(self, username):
        self.__cur.execute("select UserID FROM user where ? = Username", username)