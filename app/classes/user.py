from classes.db_queries import ConnectionInstance



class User:

    def __init__(self, email):
        self.email = email
        with ConnectionInstance() as con:
            self.id = con.get_user_id(self.email)
            self.username = con.get_username(self.email)
            self.password = con.get_pass_hash(self.email)

    def __repr__(self):
        if not self.is_anonymous():
            return '<User %r>' % self.username

    def is_authenticated(self):
            return True

    def is_active(self):
            return True

    def is_anonymous(self):
            return False

    def get_id(self):
            return str(self.email)
