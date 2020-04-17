class Campus:
    def __init__(self, id, name, category, latitude, longitude):
        self.id = id
        self.name = name
        self.category = category
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'category': self.category, 'lat': self.latitude,
                'lng': self.longitude}


class Campusses:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,name,category,latitude,longitude FROM campus")
        result = list()
        for row in cursor:
            school = Campus(row[0], row[1], row[2], row[3], row[4])
            result.append(school)
        return result

    def get_on_id(self, school_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,name,category,latitude,longitude FROM campus WHERE id=%s", (school_id,))
        # 1 result
        row = cursor[0]
        school = Campus(row[0], row[1], row[2], row[3], row[4])
        return school
