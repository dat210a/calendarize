from classes.db_queries import ConnectionInstance


class User:

    def __init__(self, email=None):
        self.authenticated = True
        self.active = True
        if email:
            self.load_user(email)

    def __repr__(self):
        if not self.is_anonymous():
            return '<User %r>' % self.username

    def is_authenticated(self):
        if self.authenticated:
            return True
        else:
            return False

    def is_active(self):
        if self.active: 
            return True
        else:
            return False

    def is_anonymous(self):
        if self.authenticated:
            return False
        else:
            return True

    def get_id(self):
        if not self.is_anonymous():
            return str(self.email)

    def load_user(self, email):
        self.email = email
        with ConnectionInstance() as con:
            self.username = con.get_username(self.email)
            self.password = con.get_pass_hash(self.email)

    def authenticate(self):
        self.authenticated = True

    def activate(self):
        self.active = True

    def deauthenticate(self):
        self.authenticate = False

    def deactivate(self):
        self.active = False

