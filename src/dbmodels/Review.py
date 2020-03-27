class Review:
    def __init__(self, id, user_for, user_from, amount_of_stars, title, review_text):
        self.id = id
        self.user_for = user_for
        self.user_from = user_from
        self.amount_of_stars = amount_of_stars
        self.title = title
        self.review_text = review_text

    def to_dict(self):
        return {'id': self.id, 'user_for': self.user_for, 'user_from': self.user_from,
                'amount_of_stars': self.amount_of_stars, 'title': self.title, 'review_text': self.review_text}


class Reviews:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id, user_for, user_from, amout_of_starts, title, review_text FROM review WHERE %s=%s",
                       (on, val))
        reviews = list()
        for row in cursor:
            review = Review(row[0], row[1], row[2], row[3], row[4], row[5])
            reviews.append(review)
        return reviews

    def get_on_id(self, id):
        found = self.get_on('id', id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_user_for(self, name):
        return self.get_on('user_for', name)

    def get_on_user_from(self, name):
        return self.get_on('user_from', name)

    def get_on_amount_of_starts(self, num):
        return self.get_on('amount_of_starts', num)

    def get_on_title(self, title):
        return self.get_on('title', title)

    # get on review text not relevant

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id, user_for, user_from, amount_of_stars, title, review_text FROM review")
        reviews = list()
        for row in cursor:
            review = Review(row[0], row[1], row[2], row[3], row[4], row[5])
            reviews.append(review)
        return reviews

    def add_review(self, review):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "review" VALUES(%s, %s, %s, %s, %s)',
                           (
                           review.user_for, review.user_from, review.amount_of_stars, review.title, review.review_text))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add review')
