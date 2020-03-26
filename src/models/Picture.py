class Picture:
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename

    def get(dbconnect, id):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,filename FROM picture WHERE id = %s", (id,))
        id, filename = cursor.fetchone()
        return Picture(id, filename)

    def get_all(dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,filename FROM picture")
        pictures = list()
        for row in cursor:
            picture = Picture(row[0], row[1])
            pictures.append(picture)
        return pictures

    def to_dict(self):
        return {'id': self.id, 'filename': self.filename}
