class Ride:
    def __init__(self, id, departure_time, arrival_time, user_id, address_to, address_from, car_id):
        # address_to & address_from are id's pointing to addresses
        self.id = id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.address_to = address_to
        self.address_from = address_from
        self.car_id = car_id

    def to_dict(self):
        return {'id': self.id, 'departure_time': self.departure_time, 'arrival_time': self.arrival_time,
                'user_id': self.user_id, 'address_to': self.address_to, 'address_from': self.address_from,
                'car_id': self.car_id}


class Rides:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id, departure_time, arrival_time, user_id, address_to, address_from, car_id FROM ride WHERE %s=%s",
                       (on, val))
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            rides.append(ride)
        return rides

    def get_on_id(self, id):
        found = self.get_on('id', id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_user_id(self, user_id):
        found = self.get_on('user_id', user_id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_car_id(self, car_id):
        found = self.get_on('car_id', car_id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_departure_time(self, departure_time):
        found = self.get_on('departure_time', departure_time)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_arrival_time(self, arrival_time):
        found = self.get_on('arrival_time', arrival_time)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_address_to(self, address_to):
        found = self.get_on('address_to', address_to)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_address_from(self, address_from):
        found = self.get_on('address_from', address_from)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,departure_time,arrival_time,user_id,address_to,address_from,car_id FROM ride")
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            rides.append(ride)
        return rides

    def add_ride(self, ride):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "ride" VALUES(default, %s, %s, %s, %s, %s, %s)',
                           (
                           ride.departure_time, ride.arrival_time, ride.user_id, ride.address_to, ride.address_from, ride.car_id))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add ride')
