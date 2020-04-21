class Address:
    def __init__(self, id, country, city, postal_code, street, nr, latitude, longitude):
        self.id = id
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.nr = nr
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {'id': self.id, 'country': self.country, 'city': self.city, 'postal_code': self.postal_code,
                'street': self.street, 'nr': self.nr, 'latitude': self.latitude, 'longitude': self.longitude}


class Addresses:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr,latitude,longitude FROM address WHERE %s=%s",
                       (on, val))
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            addresses.append(address)
        return addresses

    def get_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id,country,city,postal_code,street,nr,latitude,longitude FROM address WHERE id=%s',
                       (id,))
        address = cursor.fetchone()
        if address is None:
            return None
        address_obj = Address(address[0], address[1], address[2], address[3], address[4], address[5], address[6],
                              address[7])
        return address_obj

    def get_id(self, country, city, postal_code, street, nr):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            'SELECT id FROM address WHERE street=%s AND nr=%s AND city=%s AND postal_code=%s AND country=%s',
            (street, nr, city, postal_code, country))
        row = cursor.fetchone()
        return row[0]

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr,latitude,longitude FROM address")
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            addresses.append(address)
        return addresses

    def add_address(self, address: Address):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "address" VALUES(default, %s, %s, %s, %s, %s, %s, %s)',
                           (address.country, address.city, address.postal_code, address.street, address.nr,
                            address.latitude, address.longitude))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add address')

    def edit_address(self, address_id, street, nr, city, postal_code, country, latitude, longitude):
        cursor = self.dbconnect.get_cursor()
        address = self.get_on_id(address_id)
        address.street = street
        address.nr = nr
        address.city = city
        address.postal_code = postal_code
        address.country = country
        address.latitude = latitude
        address.longitude = longitude
        try:
            cursor.execute(
                'UPDATE "address" SET street=%s, nr=%s, city=%s, postal_code=%s, country=%s, latitude=%s, longitude=%s WHERE id=%s',
                (street, nr, city, postal_code, country, latitude, longitude, address_id))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to edit address')

    def delete_address(self, address_id):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM "address" WHERE id=%s', (address_id,))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to delete address')
