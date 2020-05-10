from postgis import *
from postgis.psycopg import register
from shapely import geometry, wkb


class PickupPoint:
    def __init__(self, id, estimated_time, coordinates, address_id, latitude=None, longitude=None):
        self.id = id,
        self.estimated_time = estimated_time
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
                'latitude': self.address.latitude,
                'longitude': self.address.longitude,
                'estimated time': self.estimated_time}

    def fetch_id(self):
        if self.id is not None:
            return self.id
        else:
            from src.utils import address_access
            self.id = address_access.get_id(self.longitude, self.latitude)
            return self.id

class PickupPoints:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, estimated_time, coordinates, address FROM pickup_point WHERE %s=%s",
            (on, val,))
        points = list()
        for row in cursor:
            ride = PickupPoint(row[0], row[1], row[2], row[3])
            points.append(ride)
        return points

    def get_id(self, latitude, longitude):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT pickup_point.id "
                       "FROM pickup_point "
                       "join address a on pickup_point.address = a.id "
                       "WHERE ST_Distance(a.coordinates, ST_MakePoint(%s, %s)) "
                       "< 50", (longitude, latitude))
        id = cursor.fetchone()[0]
        return id

    def get_on_id(self, id):
        if id is None:
            return None
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, estimated_time, coordinates, address FROM pickup_point WHERE id=%s", (id,))
        row = cursor.fetchone()
        return PickupPoint(id, row[1], row[2], row[3])

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, estimated_time, coordinates, address FROM pickup_point")
        points = list()
        for row in cursor:
            ride = PickupPoint(row[0], row[1], row[2], row[3])
            points.append(ride)
        return points

    #  def __init__(self, id, country, city, postal_code, street, nr, latitude, longitude, coordinates):
    def add_pickup_point(self, p):
        cursor = self.dbconnect.get_cursor()

        from src.utils import address_access
        from src.dbmodels.Address import Address
        the_id = address_access.add_address(Address(None, '?', '?', '?', '?', '?', p.longitude, p.latitude, None))

        cursor.execute('INSERT INTO "pickup_point" VALUES(default, %s, ST_MakePoint(%s, %s), %s)',
                       (p.estimated_time, p.longitude, p.latitude, the_id))
        self.dbconnect.commit()

    def get_distance(self, latitude, longitude, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT ST_Distance(a.coordinates, ST_MakePoint(%s, %s)) "
                       "FROM pickup_point p "
                       "join address a on p.address = a.id "
                       "where a.id=%s", (longitude, latitude, id))
        dist = cursor.fetchone()[0]
        return dist
