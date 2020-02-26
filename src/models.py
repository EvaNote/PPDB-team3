import psycopg2


# Class that represents the connection to the database.
class DBConnection:
    def __init__(self,dbname,dbuser):
        try:
            self.conn = psycopg2.connect("dbname='{}' user='{}'".format(dbname,dbuser))
        except:
            print('ERROR: Unable to connect to database')
            raise Exception('Unable to connect to database')
        
    def close(self):
        self.conn.close()
        
    def get_connection(self):
        return self.conn
    
    def get_cursor(self):
        return self.conn.cursor()
    
    def commit(self):
        return self.conn.commit()
    
    def rollback(self):
        return self.conn.rollback()


# Class that represents the "user" table from the database
class User:
    def __init__(self, first_name, last_name, email, password, joined_on=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.joined_on = joined_on
        
    def to_dct(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'joined_on': self.joined_on}


# Class used for accessing data from the "user" table from the database
class UserAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_users(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, joined_on FROM "user"')  
        users = list()
        for row in cursor:
            user_obj = User(row[0], row[1], row[2], row[3], row[4])
            users.append(user_obj)
        return users

    def add_user(self, user_obj): 
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "user" VALUES(%s, %s, %s, %s, now())', (user_obj.first_name, user_obj.last_name, user_obj.email, user_obj.password,))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add user')

