from classes.db_queries import ConnectionInstance



class User:

    def __init__(self, email):
        self.email = email
        with ConnectionInstance() as con:
            self.user_id = con.get_user_id(self.email)
            self.active = con.get_user_activity(self.email)
            self.name = con.get_user_name(self.user_id)

    def __repr__(self):
        if not self.is_anonymous():
                return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.active > 0:
            return True
        return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)
