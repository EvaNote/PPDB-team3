from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort
import flask_login
from flask_login import current_user, login_user, logout_user
from src.dbmodels.User import User
from src.reviews.forms import Reviews
from src.users.forms import LoginForm, RegistrationForm, VehicleForm
from src.utils import user_access, bcrypt, review_access

users = Blueprint('users', __name__, url_prefix='/<lang_code>')


########################################################################################################################
# functions for multilingual support
@users.url_defaults
def add_language_code(endpoint, values):
    if g.lang_code in current_app.config['SUPPORTED_LANGUAGES']:
        values.setdefault('lang_code', g.lang_code)
    else:
        values.setdefault('lang_code', 'en')


@users.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@users.before_request
def before_request():
    if g.lang_code not in current_app.config['SUPPORTED_LANGUAGES']:
        abort(404)


########################################################################################################################


@users.route("/account")
def account():
    form = Reviews()
    data = review_access.get_on_user_for(current_user.id)
    return render_template('account.html', title='Account', form=form, loggedIn=True, data=data,
                           current_user=current_user)


@users.route("/edit")
def account_edit():
    return render_template('account_edit.html', title='Edit account info', loggedIn=True)


@users.route("/myrides")
def myrides():
    return render_template('ride_history.html', title='My rides', loggedIn=True)


@users.route("/user=<userid>", methods=['GET', 'POST'])
def user(userid):
    form = Reviews()
    target_user = user_access.get_user_on_id(userid)
    data = review_access.get_on_user_for(userid)
    try:
        the_id = current_user.id
        logged_in = True
    except:
        logged_in = False
    return render_template('user.html', title='User profile', form=form, loggedIn=logged_in, target_user=target_user,
                           data=data)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # makes sure user won`t be able to go to login/register page
        return redirect(url_for('main.home'))
    form = LoginForm()
    # check if input is valid
    if form.validate_on_submit():
        user = user_access.get_user(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your email and/or password.', 'danger')
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash(f'Succesfully logged out.', 'success')  # success is for bootstrap class
    return redirect(url_for('main.home'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # makes sure user won`t be able to go to login/register page
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # check if input is valid

    if form.validate_on_submit():
        user_email = form.email.data
        user_first_name = form.first_name.data
        user_last_name = form.last_name.data
        # decode to make sure it`s a string, not bytes
        user_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_obj = User(first_name=user_first_name, last_name=user_last_name, email=user_email, password=user_password)
        user_access.add_user(user_obj)
        flash(f'Account created for {form.email.data}! You can now log in', 'success')  # success is for bootstrap class

        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


@users.route("/add_vehicle", methods=['GET', 'POST'])
def add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        flash(f'Vehicle registered!', 'success')
        return redirect(url_for('users.add_vehicle'))
    return render_template("add_vehicle.html", title="Add Vehicle", form=form)
