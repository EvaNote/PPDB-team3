from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort, request, make_response
from src.reviews.forms import ReviewForm
from flask_login import current_user
from src.dbmodels.Review import Review
from src.utils import user_access, review_access, picture_access
from flask_babel import lazy_gettext
from src.emails import *
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
    if userfor.picture is None:
        picture = "images/temp_profile_pic.png"
    else:
        picture = "images/" + str(picture_access.get_picture_on_id(userfor.picture).filename)
    if form.validate_on_submit():
        user_from = current_user.id
        user_for = userid
        amount_of_stars = form.amount_of_stars.data
        title = form.title.data
        text = form.text.data
        role = form.role.data
        if role == 0:
            role = 'driver'
        else:
            role = 'passenger'
        review_obj = Review(None, user_for, user_from, amount_of_stars, title, text, None, role)
        review_access.add_review(review_obj)
        writer = user_access.get_user_on_id(current_user.id)
        writer_name = writer.first_name + " " + writer.last_name
        user_for_ = user_access.get_user_on_id(user_for)
        user_for_email = user_for_.email
        if user_for_.send_emails:
            send_email_review(user_for_email, writer_name)
        flash(lazy_gettext('Your review has been posted successfully!'), 'success')
        return redirect(url_for('users.user',userid=userid))
    return render_template('new_review.html', title=lazy_gettext('New review'), form=form, loggedIn=True, user_from=current_user,
                           user_for=userfor, userid=userid, picture=picture)


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
            user_from = user_access.get_user_on_id(d.user_from)
            pic = "images/"
            if user_from.picture is None:
                pic += "temp_profile_pic.png"
            else:
                pic += picture_access.get_picture_on_id(user_from.picture).filename
            dict_ = d.to_dict()
            p = url_for('static', filename=pic)
            dict_["picture"] = p
            link = url_for('users.user', userid=user_from.id)
            dict_["link"] = link
            data2.append(dict_)

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
            user_from = user_access.get_user_on_id(d.user_from)
            pic = "images/"
            if user_from.picture is None:
                pic += "temp_profile_pic.png"
            else:
                pic += picture_access.get_picture_on_id(user_from.picture).filename
            dict_ = d.to_dict()
            p = url_for('static', filename=pic)
            dict_["picture"] = p
            link = url_for('users.user', userid=user_from.id)
            dict_["link"] = link
            if search_term.lower() in dict_['title'].lower():
                data2.append(dict_)
            elif search_term.lower() in dict_['review_text'].lower():
                data2.append(dict_)
            elif search_term.lower() in dict_['user_from_first_name'].lower():
                data2.append(dict_)
            elif search_term.lower() in dict_['user_from_last_name'].lower():
                data2.append(dict_)
            elif search_term.lower() in dict_['creation'].lower():
                data2.append(dict_)
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
            user_from = user_access.get_user_on_id(d.user_from)
            pic = "images/"
            if user_from.picture is None:
                pic += "temp_profile_pic.png"
            else:
                pic += picture_access.get_picture_on_id(user_from.picture).filename
            p = url_for('static', filename=pic)
            dict_ = d.to_dict()
            dict_["picture"] = p
            link = url_for('users.user',userid=user_from.id)
            dict_["link"] = link
            if me == 'true':
                if d.user_from == current_user.id:
                    data2.append(dict_)
            else:
                data2.append(dict_)
    resp = make_response(json.dumps(data2))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
