class Address:
    def __init__(self, id, country, city, postal_code, street, nr):
        self.id = id
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.nr = nr

    def get(dbconnect, id):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr FROM address WHERE id = %s", (id,))
        id, country, city, postal_code, street, nr = cursor.fetchone()
        return Address(id, country, city, postal_code, street, nr)

    def get_all(dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr FROM address")
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5])
            addresses.append(address)
        return addresses

    def to_dict(self):
        return {'id': self.id, 'country': self.country, 'city': self.city, 'postal_code': self.postal_code,
                'street': self.street, 'nr': self.nr}

class Addresses:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr FROM address WHERE %s=%s",
                       (on, val))
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5])
            addresses.append(address)
        return addresses

    def get_on_id(self, id):
        found = self.get_on('id', id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr FROM address")
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5])
            addresses.append(address)
        return addresses

    def add_address(self, address):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "address" VALUES(default, %s, %s, %s, %s, %s)',
                           (
                           address.country,address.city,address.postal_code,address.street,address.nr))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add address')
