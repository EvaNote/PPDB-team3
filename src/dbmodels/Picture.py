class Picture:
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename

    def to_dict(self):
        return {'id': self.id, 'filename': self.filename}


    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No "id" attribute - override "get_id"')

    def get_filename(self):
        try:
            return self.filename
        except AttributeError:
            raise NotImplementedError('No "filename" attribute - override "get_filename"')

class Pictures:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_picture_on_filename(self, filename):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id, filename FROM "picture" WHERE filename=%s', (filename,))
        row = cursor.fetchone()
        if row:
            result = Picture(row[0], row[1])
            return result
        return None

    def get_picture_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id, filename FROM "picture" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row:
            result = Picture(row[0], row[1])
            return result
        return None

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,filename FROM picture")
        pictures = list()
        for row in cursor:
            picture = Picture(row[0], row[1])
            pictures.append(picture)
        return pictures

    def add_picture(self, picture):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "picture" VALUES(default, %s)',
                           (picture.filename,))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add picture')