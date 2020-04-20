from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort
from src.reviews.forms import ReviewForm
from flask_login import current_user, login_user, logout_user
from src.dbmodels.Review import Reviews, Review
from src.utils import user_access, review_access
from flask_babel import lazy_gettext

reviews = Blueprint('reviews', __name__, url_prefix='/<lang_code>')


########################################################################################################################
# functions for multilingual support
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


########################################################################################################################


@reviews.route("/user=<userid>/new_review", methods=['GET', 'POST'])
def new_review(userid):
    if not userid.isdigit():
        abort(404)
    if not current_user.is_authenticated and not current_app.config[
        'TESTING']:  # makes sure user won`t be able to go to login/register page
        return redirect(url_for('users.login'))
    form = ReviewForm()
    userfor = user_access.get_user_on_id(userid)
    if form.validate_on_submit():
        user_from = current_user.id
        user_for = userid
        amount_of_stars = form.amount_of_stars.data
        title = form.title.data
        text = form.text.data
        review_obj = Review(None, user_for, user_from, amount_of_stars, title, text)
        review_access.add_review(review_obj)
        flash(lazy_gettext('Your review has been posted successfully!'), 'success')
        return redirect(url_for('main.home'))
    else:
        flash(lazy_gettext('Writing review failed.'), 'danger')
    return render_template('new_review.html', title=lazy_gettext('New review'), form=form, loggedIn=True, user_from=current_user,
                           user_for=userfor)
