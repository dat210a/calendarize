from classes.db_queries import ConnectionInstance



class User:

    def __init__(self, email):
        self.email = email
        with ConnectionInstance() as q:
            self.user_id = q.get_user_id(self.email)
            self.active = q.get_user_activity(self.email)
            self.name = q.get_user_name(self.user_id)

    def __repr__(self):
        if not self.is_anonymous():
                return '<User %r>' % self.email

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

    def username(self):
        return self.name if self.name else self.email
