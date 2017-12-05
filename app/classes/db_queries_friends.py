from classes.db_queries import ConnectionInstance
import logging

class ConnectionInstanceFriends(ConnectionInstance):


    def __init__(self):
        ConnectionInstance.__init__(self)
        self.__con = self._ConnectionInstance__con
        self.__cur = self._ConnectionInstance__cur


    def get_friends(self, uid):
        sql = "SELECT user_id, friend_id, friend_email FROM user_friends WHERE user_id = ? OR friend_id = ?"
        self.__cur.execute(sql, (uid, uid))
        try:
            return self.__cur.fetchall()
        except Exception as e:
            logging.debug('{}\nWhile fetching friends for user: {}'.format(e, uid))
            return None


    def get_friend_requests(self, email):
        sql = "SELECT user_id FROM user_friends WHERE friend_email = ?"
        self.__cur.execute(sql, (email, ))
        try:
            return self.__cur.fetchall()
        except Exception as e:
            logging.debug('{}\nWhile fetching friend requests for user with email: {}'.format(e, email))
            return None


    def check_friend(self, uid, fid, email):
        sql = "SELECT unique_id FROM user_friends WHERE user_id = ? AND (friend_id = ? OR friend_email = ?)"
        self.__cur.execute(sql, (uid, fid, email))
        try:
            res = self.__cur.fetchone()
            return res[0]
        except Exception as e:
            logging.debug('{}\nWhile checking friend for user: {}'.format(e, uid))
            return None


    def add_friend(self, uid, email):
        sql = "INSERT INTO user_friends (user_id, friend_email) VALUES (?, ?)"
        self.__cur.execute(sql, (uid, email))
        try:
            self.__con.commit()
            return self.get_last_ID()
        except Exception as e:
            logging.debug('{}\nWhile trying to add friend with data:\n'
                          '\tuser id: {}\n'
                          '\temail: {}'.format(e, uid, email))
            self.__con.rollback()
            return None

    
    def accept_friend(self, uid, fid, email):
        sql = "UPDATE user_friends SET friend_id = ?, friend_email = NULL WHERE user_id = ? AND friend_email = ?"
        self.__cur.execute(sql, (fid, uid, email))
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile accepting friend request with id:\n{}'.format(e, uid))
            self.__con.rollback()
            return False


    def remove_friend(self, unique_id):
        sql = "DELETE FROM user_friends WHERE unique_id = ?"
        self.__cur.execute(sql, (unique_id, ))
        try:
            self.__con.commit()
            return True
        except Exception as e:
            logging.debug('{}\nWhile trying to remove friend with row id: {}'.format(e, unique_id))
            self.__con.rollback()
            return False
