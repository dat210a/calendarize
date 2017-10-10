class User:
    is_authenticated = False
    is_active = False
    is_anonymous = False
    __user_id = 0

    def __init__(self, user_id):
        self.__user_id = user_id

    def get_id(self):
        return self.__user_id