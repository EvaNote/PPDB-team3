class Address:
    def __init__(self, id, country, city, postal_code, street, nr):
        self.id = id
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.nr = nr

    def get(cursor, id):
        cursor.execute("SELECT id,country,city,postal_code,street,nr FROM address WHERE id = %s", (id,))
        id,country,city,postal_code,street,nr = cursor.fetchone()
        return Address(id,country,city,postal_code,street,nr)

    def to_dict(self):
        return {'id': self.id, 'country': self.country, 'city': self.city, 'postal_code': self.postal_code,
        'street': self.street, 'nr': self.nr}
