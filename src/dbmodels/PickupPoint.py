class PickupPoint:
    def __init__(self, id, latitude, longitude, estimated_time):
        self.id = id,
        self.latitude = latitude
        self.longitude = longitude
        self.estimated_time = estimated_time

    def to_dict(self):
        return {'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude,
                'estimated time': self.estimated_time}


class PickupPoints:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, latitude, longitude, estimated_time FROM pickup_point WHERE %s=%s",
            (on, val,))
        points = list()
        for row in cursor:
            ride = PickupPoint(row[0], row[1], row[2], row[3])
            points.append(ride)
        return points

    def get_id(self, latitude, longitude):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id FROM pickup_point WHERE latitude=%s AND longitude=%s", (latitude, longitude))
        id = cursor.fetchone()[0]
        return id

    def get_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, latitude, longitude, estimated_time FROM pickup_point WHERE id=%s", (id,))
        row = cursor.fetchone()
        return PickupPoint(id, row[1], row[2], row[3])

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, latitude, longitude, estimated_time FROM pickup_point")
        points = list()
        for row in cursor:
            ride = PickupPoint(row[0], row[1], row[2], row[3])
            points.append(ride)
        return points

    def add_pickup_point(self, p):
        cursor = self.dbconnect.get_cursor()

        cursor.execute('INSERT INTO "pickup_point" VALUES(default, %s, %s, %s)', (p.latitude, p.longitude, p.estimated_time))
        self.dbconnect.commit()
