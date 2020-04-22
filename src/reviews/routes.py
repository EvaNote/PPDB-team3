from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort, request, make_response
from src.reviews.forms import ReviewForm
from flask_login import current_user
from src.dbmodels.Review import Review
from src.utils import user_access, review_access
from flask_babel import lazy_gettext
import json

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
    # makes sure user won`t be able to go to login/register page
    if not current_user.is_authenticated and not current_app.config['TESTING']:
        return redirect(url_for('users.login'))
    form = ReviewForm()
    userfor = user_access.get_user_on_id(userid)
    if form.validate_on_submit():
        user_from = current_user.id
        user_for = userid
        amount_of_stars = form.amount_of_stars.data
        title = form.title.data
        text = form.text.data
        review_obj = Review(None, user_for, user_from, amount_of_stars, title, text, None)
        review_access.add_review(review_obj)
        flash(lazy_gettext('Your review has been posted successfully!'), 'success')
        return redirect(url_for('users.user',userid=userid))
    # else:
    #     flash(lazy_gettext('Writing review failed.'), 'danger')
    return render_template('new_review.html', title=lazy_gettext('New review'), form=form, loggedIn=True, user_from=current_user,
                           user_for=userfor)


@reviews.route("/sort", methods=['POST'])
def sort():
    order = request.form['order']
    u_id = request.form['user']
    select = request.form['select']
    select = select.split('|')
    if len(select) == 1:
        select = []
    data = review_access.get_on_user_for(u_id)
    if order == 'Rate Low-High':
        data = sorted(data, key=lambda review: review.amount_of_stars)
    elif order == 'Rate High-Low':
        data = sorted(data, key=lambda review: review.amount_of_stars, reverse=True)
    elif order == 'Date Old-New':
        data = sorted(data, key=lambda review: review.creation)
    else:
        data = sorted(data, key=lambda review: review.creation, reverse=True)
    data2 = list()
    for d in data:
        if str(d.id) in select or len(select) == 0:
            data2.append(d.to_dict())
    resp = make_response(json.dumps(data2))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@reviews.route("/search", methods=['POST'])
def search():
    search_term = request.form['search']
    u_id = request.form['user']
    select = request.form['select']
    select = select.split('|')
    if len(select) == 1:
        select = []
    data = review_access.get_on_user_for(u_id)
    data2 = list()
    for d in data:
        if str(d.id) in select or len(select) == 0:
            d = d.to_dict()
            if search_term.lower() in d['title'].lower():
                data2.append(d)
            elif search_term.lower() in d['review_text'].lower():
                data2.append(d)
            elif search_term.lower() in d['user_from_first_name'].lower():
                data2.append(d)
            elif search_term.lower() in d['user_from_last_name'].lower():
                data2.append(d)
            elif search_term.lower() in d['creation'].lower():
                data2.append(d)
    resp = make_response(json.dumps(data2))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@reviews.route("/filterstars", methods=['POST'])
def filter_stars():
    stars = request.form['stars']
    u_id = request.form['user']
    me = request.form['writtenByMe']
    data = review_access.get_on_user_for(u_id)
    data2 = list()
    for d in data:
        if str(d.amount_of_stars) in stars or len(stars) == 0:
            if me == 'true':
                if d.user_from == current_user.id:
                    data2.append(d.to_dict())
            else:
                data2.append(d.to_dict())
    resp = make_response(json.dumps(data2))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
