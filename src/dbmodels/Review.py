from datetime import date

class Review:
    def __init__(self, id, user_for, user_from, amount_of_stars, title, review_text, creation):
        self.id = id
        self.user_for = user_for
        self.user_from = user_from
        self.amount_of_stars = amount_of_stars
        self.title = title
        self.review_text = review_text
        self.creation = creation

    def to_dict(self):
        return {'id': self.id, 'user_for': self.user_for, 'user_from': self.user_from,
                'amount_of_stars': self.amount_of_stars, 'title': self.title, 'review_text': self.review_text}

    def get_user_from_as_object(self):
        from src.utils import user_access
        return user_access.get_user_on_id(self.user_from)

    def get_creation_date_as_string(self):
        year = self.creation.year
        month = self.creation.month
        day = self.creation.day
        # add '?' as dummy because first month is january (not 0th)
        months = ['?', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        day_add = ''
        if day % 10 == 1:
            day_add = 'st'
        elif day % 10 == 2:
            day_add = 'nd'
        else:
            day_add = 'th'
        return months[month] + ' ' + str(day) + day_add + ', ' + str(year)


class Reviews:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, user_for, user_from, amount_of_stars, title, review_text, creation FROM review WHERE %s=%s",
            (on, val))
        reviews = list()
        for row in cursor:
            review = Review(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            reviews.append(review)
        return reviews

    def get_on_id(self, id):
        found = self.get_on('id', id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_user_for(self, the_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, user_for, user_from, amount_of_stars, title, review_text, creation FROM review WHERE user_for=%s",
            (the_id,))
        reviews = list()
        for row in cursor:
            review = Review(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            reviews.append(review)
            print(review)
        return reviews
        # return self.get_on('user_for', the_id)

    def get_on_user_from(self, the_id):
        return self.get_on('user_from', the_id)

    def get_on_amount_of_starts(self, num):
        return self.get_on('amount_of_starts', num)

    def get_on_title(self, title):
        return self.get_on('title', title)

    # get on review text not relevant

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id, user_for, user_from, amount_of_stars, title, review_text, creation FROM review")
        reviews = list()
        for row in cursor:
            review = Review(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            reviews.append(review)
        return reviews

    def add_review(self, review):
        cursor = self.dbconnect.get_cursor()
        try:
            print(review.user_for)
            print(review.user_from)
            print(review.amount_of_stars)
            print(review.title)
            print(review.review_text)
            cursor.execute('INSERT INTO "review" VALUES(default, %s, %s, %s, %s, %s, default)',
                           (
                           review.user_for, review.user_from, review.amount_of_stars, review.title, review.review_text))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add review')
