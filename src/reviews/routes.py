from flask import Blueprint, render_template, g, current_app, abort
from src.reviews.forms import ReviewForm

reviews = Blueprint('reviews', __name__, url_prefix='/<lang_code>')


@reviews.url_defaults
def add_language_code(endpoint, values):
    if g.lang_code in current_app.config['SUPPORTED_LANGUAGES']:
        values.setdefault('lang_code', g.lang_code)
    else:
        values.setdefault('lang_code', 'en')


@reviews.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@reviews.before_request
def before_request():
    if g.lang_code not in current_app.config['SUPPORTED_LANGUAGES']:
        abort(404)


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
