from mysql import connector

class DatabaseQueries:

    __cur = connector.connect().cursor()
    __con = connector.connect()

    def __init__(self):
        self.con = connector.connect(user="admin", password="admin", host="127.0.0.1", database="Calander")
        self.cur = self.con.cursor()


    def __enter__(self):
        return self.__cur


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__con.close()