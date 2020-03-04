class Picture:
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename

    def get(cursor, id):
        cursor.execute("SELECT id,filename FROM picture WHERE id = %s", (id,))
        id,filename = cursor.fetchone()
        return Picture(id,filename)

    def to_dict(self):
        return {'id': self.id, 'filename': self.filename}
