from flask import Blueprint, render_template
from src.reviews.forms import ReviewForm

reviews = Blueprint('reviews', __name__)


@reviews.route("/newreview", methods=['GET', 'POST'])
def newreview():
    form = ReviewForm()
    return render_template('new_review.html', title='New review', form=form, loggedIn=True)

# @reviews.route("/reviews", methods=['GET', 'POST'])
# def reviews():
#     form = Reviews()
#     return render_template("my_reviews.html", title='My Reviews', form=form, loggedIn=True)
#
#
# @reviews.route("/exampleuser/reviews", methods=['GET', 'POST'])
# def exampleuser_reviews():
#     form = Reviews()
#     return render_template("my_reviews.html", title='Reviews of example user', form=form, loggedIn=True)
