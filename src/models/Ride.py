class Ride:
    def __init__(self, id, departure_time, arrival_time, user_id, address_to, address_from):
        # address_to & address_from are id's pointing to addresses
        self.id = id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.address_to = address_to
        self.address_from = address_from

    def get(cursor, id):
        cursor.execute("SELECT id,departure_time,arrival_time,user_id,address_to,address_from FROM ride WHERE id = %s", (id,))
        id,departure_time,arrival_time,user_id,address_to,address_from = cursor.fetchone()
        return Ride(id,departure_time,arrival_time,user_id,address_to,address_from)

    def to_dict(self):
        return {'id': self.id, 'departure_time': self.departure_time, 'arrival_time': self.arrival_time,
        'user_id': self.user_id, 'address_to': self.address_to, 'address_from': self.address_from}
