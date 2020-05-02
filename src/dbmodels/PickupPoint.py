from postgis import *
from postgis.psycopg import register
from shapely import geometry, wkb


class PickupPoint:
    def __init__(self, id, latitude, longitude, estimated_time, coordinates):
        self.id = id,
        self.estimated_time = estimated_time
        if coordinates:
            self.coordinates = wkb.loads(coordinates, hex=True)
            self.latitude = self.coordinates.y
            self.longitude = self.coordinates.x
        else:
            self.coordinates = wkb.dumps(coordinates, hex=True)
            self.latitude = latitude
            self.longitude = longitude

    def to_dict(self):
        return {'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude,
                'estimated time': self.estimated_time}


class PickupPoints:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, latitude, longitude, estimated_time, coordinates FROM pickup_point WHERE %s=%s",
            (on, val,))
        points = list()
        for row in cursor:
            ride = PickupPoint(row[0], row[1], row[2], row[3], row[4])
            points.append(ride)
        return points

    def get_id(self, latitude, longitude):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id FROM pickup_point WHERE ST_Distance(pickup_point.coordinates, ST_MakePoint(%s, %s)) "
                       "< 50", (longitude, latitude))
        id = cursor.fetchone()[0]
        return id

    def get_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, latitude, longitude, estimated_time, coordinates FROM pickup_point WHERE id=%s", (id,))
        row = cursor.fetchone()
        return PickupPoint(id, row[1], row[2], row[3], row[4])

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, latitude, longitude, estimated_time, coordinates FROM pickup_point")
        points = list()
        for row in cursor:
            ride = PickupPoint(row[0], row[1], row[2], row[3], row[4])
            points.append(ride)
        return points

    def add_pickup_point(self, p):
        cursor = self.dbconnect.get_cursor()

        cursor.execute('INSERT INTO "pickup_point" VALUES(default, %s, %s, %s, ST_MakePoint(%s, %s))',
                       (p.latitude, p.longitude, p.estimated_time, p.longitude, p.latitude))
        self.dbconnect.commit()

    def get_distance(self, latitude, longitude, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT ST_Distance(pickup_point.coordinates, ST_MakePoint(%s, %s)) FROM pickup_point WHERE id=%s"
            , (longitude, latitude, id))
        dist = cursor.fetchone()[0]
        return dist
