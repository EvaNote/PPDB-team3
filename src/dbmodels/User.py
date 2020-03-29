import sys
# user_loader expects user_model to have certain attributes and methods: isAuthenticated, isActive, isAnonymous, getID
from flask_login import UserMixin


# Class that represents the "user" table from the database
class User:
    def __init__(self, first_name, last_name, email, password, id):
        # gender is M or F, active_since is a date, address & picture are id's that reference an address & picture
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.age = 1
        self.gender = 'M'
        self.joined_on = None
        self.picture = None
        self.address = None

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
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """

        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    if sys.version_info[0] != 2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

    def to_dict(self):
        return {'id': None, ' email': self.email, 'first_name': self.first_name, 'last_name': self.last_name,
                'age': self.age, 'gender': self.gender, 'joined_on': self.joined_on, 'picture': self.picture,
                'address': self.address}


# Class used for accessing data from the "user" table from the database
class UserAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_users(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, id FROM "user"')
        users = list()
        for row in cursor:
            user_obj = User(row[0], row[1], row[2], row[3], row[4])
            users.append(user_obj)
        return users

    def get_user(self, em):
        print(em)
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, id FROM "user" WHERE email=%s', (em,))
        row = cursor.fetchone()
        if row:
            result = User(row[0], row[1], row[2], row[3], row[4])
            result.id = row[4]
            return result
        return None

    def get_user_on_id(self, theId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password FROM "user" WHERE id=%s', (theId,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    def add_user(self, user_obj):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "user" VALUES(default, %s, %s, %s, %s, now(), %s, %s)',
                           (user_obj.first_name, user_obj.last_name, user_obj.email, user_obj.password, user_obj.age,
                            user_obj.gender))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add user')
