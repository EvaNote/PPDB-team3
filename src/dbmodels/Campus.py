from postgis import *
from postgis.psycopg import register
from shapely import geometry, wkb


class Campus:
    def __init__(self, id, name, category, coordinates, address_id, latitude=None, longitude=None):
        self.id = id
        self.name = name
        self.category = category
        from src.utils import address_access
        self.address = address_access.get_on_id(address_id)
        if coordinates:
            self.coordinates = wkb.loads(coordinates, hex=True)
            self.latitude = self.coordinates.y
            self.longitude = self.coordinates.x
        else:
            self.coordinates = wkb.dumps(coordinates, hex=True)
            self.latitude = latitude
            self.longitude = longitude

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'category': self.category,
                'lat': self.address.latitude,
                'lng': self.address.longitude}


class Campusses:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,name,category,coordinates,address FROM campus")
        result = list()
        for row in cursor:
            school = Campus(row[0], row[1], row[2], row[3], row[4])
            result.append(school)
        return result

    def get_on_id(self, school_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,name,category,coordinates,address FROM campus WHERE id=%s",
                       (school_id,))
        # 1 result
        row = cursor.fetchone()
        if row:
            school = Campus(row[0], row[1], row[2], row[3], row[4])
            return school
        else:
            return None

    def get_name_if_exists(self, lat, lng):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT campus.id "
                       "FROM campus "
                       "join address a on campus.address = a.id "
                       "WHERE ST_Distance(a.coordinates, ST_MakePoint(%s, %s)) "
                       "< 50", (lng, lat))
        # 1 result
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return ''

    def is_campus(self, lat, lng):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT campus.id "
                       "FROM campus "
                       "join address a on campus.address = a.id "
                       "WHERE ST_Distance(a.coordinates, ST_MakePoint(%s, %s)) "
                       "< 200", (lng, lat))
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchone()[0]

    def get_distance(self, latitude, longitude, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT ST_Distance(a.coordinates, ST_MakePoint(%s, %s)) "
                       "FROM campus "
                       "join address a on campus.address = a.id "
                       "where campus.id=%s", (longitude, latitude, id))
        dist = cursor.fetchone()[0]
        return dist
