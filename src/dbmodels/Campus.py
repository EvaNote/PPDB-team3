class Campus:
    def __init__(self, id, name, category, address_id):
        self.id = id
        self.name = name
        self.category = category
        self.address_id = address_id

    def to_dict(self):
        from src.utils import address_access
        addr = address_access.get_on_id(self.address_id).to_dict()
        return {'id': self.id, 'name': self.name, 'category': self.category, 'address': addr, 'lat': addr['latitude'],
                'lng': addr['longitude']}


class Campusses:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect
        # add campuses if needed
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT * FROM campus")
        if not cursor.fetchone():
            ref_id = None
            from src.utils import address_access
            from src.dbmodels.Address import Address
            file = open('src/dbmodels/campusses.txt', 'r')
            line = file.readline()
            name = ''
            type = ''
            lat = ''
            lng = ''
            street = ''
            city = ''
            nr = ''
            postcode = ''
            while line:
                line = "".join(line.split("'"))
                line = "".join(line.split("\n"))
                if line.startswith('name'):
                    name = line[6:]
                elif line.startswith('type'):
                    type = line[6:]
                elif line.startswith('lng'):
                    lng = line[5:]
                elif line.startswith('lat'):
                    lat = line[5:]
                elif line.startswith('street'):
                    street = line[8:]
                elif line.startswith('nr'):
                    nr = line[4:]
                elif line.startswith('postcode'):
                    postcode = line[10:]
                elif line.startswith('city'):
                    city = line[6:]
                    address_access.add_address(Address(None, 'Belgium', city, postcode, street, nr, lat, lng))
                    if not ref_id:
                        ref_id = address_access.get_latest_id()
                    else:
                        ref_id += 1
                    cursor = self.dbconnect.get_cursor()
                    try:
                        cursor.execute('INSERT INTO "campus" VALUES(default, %s, %s, %s)',
                                       (name, type, ref_id))
                        self.dbconnect.commit()
                    except:
                        raise Exception('Unable to add campus')
                    type = ''
                    lat = ''
                    lng = ''
                    street = ''
                    city = ''
                    nr = ''
                    postcode = ''
                line = file.readline()
            file.close()

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,name,category,address_id FROM campus")
        result = list()
        for row in cursor:
            school = Campus(row[0], row[1], row[2], row[3])
            result.append(school)
        return result

    def get_on_id(self, school_id):
        print('------------------------------------------', school_id)
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,name,category,address_id FROM campus WHERE id=%s", (school_id,))
        # 1 result
        row = cursor.fetchone()
        school = Campus(row[0], row[1], row[2], row[3])
        return school

    def get_name_if_exists(self, from_lat, from_lng):
        from src.utils import address_access
        addr = address_access.get_on_lat_lng(from_lat, from_lng)
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT name FROM campus WHERE address_id=%s", (addr.id,))
        # 1 result
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return ''

    def is_campus(self, lat, lng):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
                SELECT c.id FROM campus as c join address as a on c.address_id = a.id 
                WHERE distance_difference(%s, %s, a.latitude, a.longitude) <= 1000
                ORDER BY distance_difference(%s, %s, a.latitude, a.longitude) LIMIT 1""", (lat, lng, lat, lng))
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchone()[0]
