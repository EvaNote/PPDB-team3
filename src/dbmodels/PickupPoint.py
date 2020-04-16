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

    # TODO add functions
