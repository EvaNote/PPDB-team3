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
        row = cursor.fetchone()
        school = Campus(row[0], row[1], row[2], row[3], row[4])
        return school

    def get_name_if_exists(self, lat, lng):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT name FROM campus WHERE latitude=%s and longitude=%s", (lat, lng,))
        # 1 result
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return ''

    def is_campus(self, lat, lng):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
                SELECT c.id FROM campus as c WHERE distance_difference(%s, %s, c.latitude, c.longitude) <= 1000
                ORDER BY distance_difference(%s, %s, c.latitude, c.longitude) LIMIT 1""", (lat, lng, lat, lng))
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchone()[0]
