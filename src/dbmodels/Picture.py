class Picture:
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename

    def to_dict(self):
        return {'id': self.id, 'filename': self.filename}


class Pictures:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id, filename FROM picture WHERE %s=%s",
                       (on, val))
        pictures = list()
        for row in cursor:
            picture = Picture(row[0], row[1])
            pictures.append(picture)
        return pictures

    def get_on_id(self, id):
        found = self.get_on('id', id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,filename FROM picture")
        pictures = list()
        for row in cursor:
            picture = Picture(row[0], row[1])
            pictures.append(picture)
        return pictures

    def add_picture(self, picture):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "picture" VALUES(%s)',
                           (
                           picture.filename))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add picture')
