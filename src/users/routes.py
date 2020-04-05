from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app, abort, request
import flask_login
from flask_login import current_user, login_user, logout_user
from src.dbmodels.User import User
from src.dbmodels.Car import Car
from src.dbmodels.Address import Address
from src.reviews.forms import Reviews
from src.users.forms import LoginForm, RegistrationForm, VehicleForm, EditAccountForm, EditAddressForm, DeleteUserForm
from src.utils import user_access, bcrypt, review_access, car_access, address_access

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
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))

    form = Reviews()
    data = review_access.get_on_user_for(current_user.id)
    cars = car_access.get_on_user_id(current_user.id)
    user = user_access.get_user_on_id(current_user.id)
    address = address_access.get_on_id(user.address)
    return render_template('account.html', title='Account', form=form, loggedIn=True, data=data,
                           current_user=user, cars=cars, address=address)


@users.route("/edit", methods=['GET', 'POST'])
def account_edit():
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
    form = EditAccountForm()
    delete_form = DeleteUserForm()
    if request.method != 'POST':
        user = user_access.get_user_on_id(current_user.id)
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.gender.data = user.gender
        form.age.data = user.age
        form.phone_number.data = user.phone_number

        return render_template('account_edit.html', title='Edit account info', loggedIn=True, form=form, delete_form=delete_form)

    if delete_form.validate_on_submit():
        user = user_access.get_user_on_id(current_user.id)
        user_access.delete_user(user.id)
        address_id = user.address
        if address_id != None:
            address = address_access.get_on_id(address_id)
            address_access.delete_address(address.id)
        cars = car_access.get_on_user_id(user.id)
        if cars != None:
            for car in cars:
                car_access.delete_car(car.id)
        flash(f'Account deleted!', 'success')
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        gender = form.gender.data
        age = form.age.data
        phone_number = form.phone_number.data
        user = user_access.get_user_on_id(current_user.id)

        user_access.edit_user(current_user.id, first_name, last_name, email, gender, age, phone_number, user.address)
        flash(f'Account edited!', 'success')
        return redirect(url_for('users.account'))
    return render_template('account_edit.html', title='Edit account info', loggedIn=True, form=form, delete_form=delete_form)

@users.route("/edit_address", methods=['GET', 'POST'])
def address_edit():
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
    form = EditAddressForm()
    if request.method != 'POST':
        user = user_access.get_user_on_id(current_user.id)
        if user.address is None:
            form.street.data = " "
            form.nr.data = " "
            form.city.data = " "
            form.postal_code.data = " "
            form.country.data = " "
        else:
            address = address_access.get_on_id(user.address)
            form.street.data = address.street
            form.nr.data = address.nr
            form.city.data = address.city
            form.postal_code.data = address.postal_code
            form.country.data = address.country
        return render_template('address_edit.html', title='Edit address', loggedIn=True, form=form)

    if form.validate_on_submit():
        street = form.street.data
        nr = form.nr.data
        city = form.city.data
        postal_code = form.postal_code.data
        country = form.country.data

        address_id = None
        user = user_access.get_user_on_id(current_user.id)
        if user.address is None:
            address_obj = Address(None, country, city, postal_code, street, nr)
            address_access.add_address(address_obj)
            address_id = address_access.get_id(country, city, postal_code, street, nr)
        else:
            address = address_access.get_on_id(user.address)
            address_access.edit_address(address.id,street,nr,city,postal_code,country)
            address_id = address.id

        user = user_access.get_user_on_id(current_user.id)
        user_access.edit_user(user.id,user.first_name,user.last_name,user.email,user.gender,user.age,user.phone_number,address_id)
        flash(f'Address edited!', 'success')
        return redirect(url_for('users.account'))
    return render_template('address_edit.html', title='Edit address', loggedIn=True, form=form)



@users.route("/myrides")
def myrides():
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
    return render_template('ride_history.html', title='My rides', loggedIn=True)


@users.route("/user=<userid>")
def user(userid):
    form = Reviews()
    target_user = user_access.get_user_on_id(userid)
    data = review_access.get_on_user_for(userid)
    return render_template('user.html', title='User profile', form=form, loggedIn=False, target_user=target_user,
                           data=data)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # makes sure user won`t be able to go to login/register page
        return redirect(url_for('main.home'))
    form = LoginForm()
    # check if input is valid
    if form.validate_on_submit():
        user = user_access.get_user_on_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your email and/or password.', 'danger')
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
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
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
    form = VehicleForm()
    if form.validate_on_submit():
        brand = form.brand.data
        model = form.model.data
        color = form.color.data
        plateNumber = form.plateNumber.data
        seats = form.seats.data
        constructionYear = form.constructionYear.data
        consumption = form.consumption.data
        fuelType = form.fuelType.data
        car_obj = Car(None, plateNumber, color, brand, model, seats, constructionYear, consumption, fuelType, current_user.id, None)
        car_access.add_car(car_obj)
        flash(f'Vehicle registered!', 'success')
        return redirect(url_for('users.account'))
    return render_template("add_vehicle.html", title="Add Vehicle", form=form)

@users.route("/edit_vehicle=<car_id>", methods=['GET', 'POST'])
def edit_vehicle(car_id):
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))
    form = VehicleForm()
    if request.method != 'POST':
        car = car_access.get_on_id(car_id)
        form.brand.data = car.brand
        form.model.data = car.model
        form.color.data = car.color
        form.plateNumber.data = car.number_plate
        form.seats.data = car.nr_seats
        form.constructionYear.data = car.construction_year
        form.consumption.data = car.fuel_consumption
        form.fuelType.data = car.fuel

        return render_template('car_edit.html', title='Edit car', loggedIn=True, form=form, car_id=car_id)

    if form.validate_on_submit():
        brand = form.brand.data
        model = form.model.data
        color = form.color.data
        plateNumber = form.plateNumber.data
        seats = form.seats.data
        constructionYear = form.constructionYear.data
        consumption = form.consumption.data
        fuelType = form.fuelType.data

        car_access.edit_car(car_id, brand, model, color, plateNumber, seats, constructionYear, consumption, fuelType)
        flash(f'Car edited!', 'success')
        return redirect(url_for('users.account'))
    return render_template('car_edit.html', title='Edit car', loggedIn=True, form=form, car_id=car_id)

@users.route("/delete_vehicle=<car_id>", methods=['GET', 'POST'])
def delete_vehicle(car_id):
    if not current_user.is_authenticated:  # makes sure user won`t be able to go to page without logging in
        return redirect(url_for('users.login'))

    car_access.delete_car(car_id)
    flash(f'Vehicle deleted!', 'success')
    return redirect(url_for('users.account'))
