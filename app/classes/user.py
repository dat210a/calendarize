class User():

    def __init__(self, uid):
        self.uid = uid

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
            return str(self.uid)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)