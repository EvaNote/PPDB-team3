class PickupPointRide:
    def __init__(self, id, pickup_point_id, ride_id):
        self.id = id,
        self.pickup_point_id = pickup_point_id
        self.ride_id = ride_id

    def to_dict(self):
        return {'id': self.id, 'pickup_point_id': self.pickup_point_id, 'ride_id': self.ride_id}


class PickupPointsRides:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    # TODO add functions