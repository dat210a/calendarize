from classes.db_queries import ConnectionInstance



class User:

    def __init__(self, email):
        self.email = email
        with ConnectionInstance() as con:
            self.user_id = con.get_user_id(self.email)
            self.username = con.get_username(self.email)
            self.active = con.get_user_activity(self.email)

    def __repr__(self):
        if not self.is_anonymous():
                return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        # change this when verification complete:
        # return self.active
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)
