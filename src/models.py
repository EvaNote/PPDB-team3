import sys

from src import connection, login_manager
from flask_login import UserMixin #user_loader expects user_model to have certain attributes and methods: isAuthenticated, isActive,isAnonymous,getID


@login_manager.user_loader
def load_user(user_email):
    return UserAccess(connection).get_user(user_email)

# Class that represents the "user" table from the database
class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def to_dct(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'joined_on': self.joined_on}
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        try:
            return self.email
        except AttributeError:
            raise NotImplementedError('No "email" attribute - override "get_id"')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''

        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    if sys.version_info[0] != 2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

# Class used for accessing data from the "user" table from the database
class UserAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_users(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password FROM "user"')
        users = list()
        for row in cursor:
            user_obj = User(row[0], row[1], row[2], row[3])
            users.append(user_obj)
        return users

    def get_user(self, em):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password FROM "user" WHERE email=%s', (em,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    def add_user(self, user_obj): 
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "user" VALUES(%s, %s, %s, %s, now())', (user_obj.first_name, user_obj.last_name, user_obj.email, user_obj.password))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add user')



