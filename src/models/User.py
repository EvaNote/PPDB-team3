class User:
    def __init__(self, id, email, first_name, last_name, age, gender, active_since, picture, address):
        # gender is M or F, active_since is a date, address & picture are id's that reference an address & picture
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.active_since = active_since
        self.picture = picture
        self.address = address

    def get(dbconnect, id):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,email,first_name,last_name,age,gender,active_since,picture,address FROM user WHERE id = %s", (id,))
        id,email,first_name,last_name,age,gender,active_since,picture,address = cursor.fetchone()
        return User(id,email,first_name,last_name,age,gender,active_since,picture,address)

    def get_all(dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,email,first_name,last_name,age,gender,active_since,picture,address FROM user")
        users = list()
        for row in cursor:
            user = User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            users.append(user)
        return users


    def to_dict(self):
        return {'id': self.id, ' email': self.email, 'first_name': self.first_name, 'last_name': self.last_name,
        'age': self.age, 'gender': self.gender, 'active_since': self.active_since, 'picture': self.picture, 'address': self.address}
