from classes.db_queries import ConnectionInstance

class User():



    def __init__(self, username,app):
        self.username = username
        with ConnectionInstance(app) as con:
            self.password = con.get_pass_hash(self.username)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)