from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort
from src.reviews.forms import Reviews
from src.users.forms import LoginForm, RegistrationForm, VehicleForm

users = Blueprint('users', __name__, url_prefix='/<lang_code>')


@users.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@users.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@users.before_request
def before_request():
    if g.lang_code not in current_app.config['SUPPORTED_LANGUAGES']:
        abort(404)


@users.route("/account")
def account():
    form = Reviews()
    return render_template('account.html', title='Account', form=form, loggedIn=True)


@users.route("/edit")
def account_edit():
    return render_template('account_edit.html', title='Edit account info', loggedIn=True)


@users.route("/myrides")
def myrides():
    return render_template('ride_history.html', title='My rides', loggedIn=True)


@users.route("/user")
def user():
    form = Reviews()
    return render_template('user.html', title='User profile', form=form, loggedIn=False)


@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # check if input is valid
    if form.validate_on_submit():
        # TODO delete this login
        if form.email.data == 'admin@login.com' and form.password.data == 'admin':
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your email and/or password.', 'danger')
    return render_template("login.html", title="Login", form=form, loggedIn=False)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # check if input is valid

    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}.', 'success')
        return redirect(url_for('main.home'))
    return render_template("register.html", title="Register", form=form, loggedIn=False)


@users.route("/add_vehicle", methods=['GET', 'POST'])
def add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        flash(f'Vehicle registered!', 'success')
        return redirect(url_for('users.add_vehicle'))
    return render_template("add_vehicle.html", title="Add Vehicle", form=form)
