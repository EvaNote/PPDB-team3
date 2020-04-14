class PickupPoint:
    def __init__(self, id, latitude, longitude):
        self.id = id,
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude}


class PickupPoints:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    # TODO add functions
