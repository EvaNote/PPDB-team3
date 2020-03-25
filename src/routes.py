from flask import render_template, url_for, flash, redirect, jsonify
from src import app, bcrypt
from src.forms import *
<<<<<<< HEAD

=======
from src.models import User, UserAccess
from flask_login import login_user, current_user, logout_user
from src import connection
>>>>>>> Login
@app.route("/")
@app.route("/home")
def home():
    #return render_template('home.html', users=UserAccess(connection).get_users(), loggedIn=False)
    return render_template('home.html', users=UserAccess(connection).get_users())


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ')


@app.route("/contact")
def contact():
    return render_template('contact.html', title='contact')


@app.route("/account")
def account():
<<<<<<< HEAD
    form = Reviews()
    return render_template('account.html', title='Account', form=form, loggedIn=True)
=======
    return render_template('account.html', title='Account')
>>>>>>> Login


@app.route("/edit")
def account_edit():
    return render_template('account_edit.html', title='Edit account info')


@app.route("/myrides")
def myrides():
    return render_template('ride_history.html', title='My rides')


@app.route("/user")
def user():
<<<<<<< HEAD
    form = Reviews()
    return render_template('user.html', title='User profile', form=form, loggedIn=False)
=======
    return render_template('user.html', title='User profile')
>>>>>>> Login


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # makes sure user won`t be able to go to login/register page
        return redirect(url_for('home'))
    form = RegistrationForm()
    # check if input is valid

    if form.validate_on_submit():
        user_email = form.email.data
        user_first_name = form.first_name.data
        user_last_name = form.last_name.data
        user_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #decode to make sure it`s a string, not bytes

        user_obj = User(first_name=user_first_name, last_name=user_last_name, email=user_email, password=user_password)
        UserAccess(connection).add_user(user_obj)
        flash(f'Account created for {form.email.data}! You can now log in', 'success') # success is for bootstrap class

        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/ride_info")
def ride_details():
    return render_template("ride_information.html", title="Ride information")


@app.route("/ride_history")
def ride_history():
    return render_template("ride_history.html", title="Ride history")


@app.route("/add_vehicle", methods=['GET', 'POST'])
def add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        flash(f'Vehicle registered!', 'success')
        return redirect(url_for('add_vehicle'))
    return render_template("add_vehicle.html", title="Add Vehicle", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:      # makes sure user won`t be able to go to login/register page
        return redirect(url_for('home'))
    form = LoginForm()
    # check if input is valid
    if form.validate_on_submit():
        user = UserAccess(connection).get_user(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect( url_for('home'))
        else:
            flash('Login failed. Please check your email and/or password.', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/newreview", methods=['GET', 'POST'])
def newreview():
    form = ReviewForm()
    return render_template('new_review.html', title='New review', form=form)


<<<<<<< HEAD
# @app.route("/reviews", methods=['GET', 'POST'])
# def reviews():
#     form = Reviews()
#     return render_template("my_reviews.html", title='My Reviews', form=form, loggedIn=True)
#
#
# @app.route("/exampleuser/reviews", methods=['GET', 'POST'])
# def exampleuser_reviews():
#     form = Reviews()
#     return render_template("my_reviews.html", title='Reviews of example user', form=form, loggedIn=True)
=======
@app.route("/reviews", methods=['GET', 'POST'])
def reviews():
    form = Reviews()
    return render_template("my_reviews.html", title='My Reviews', form=form)


@app.route("/exampleuser/reviews", methods=['GET', 'POST'])
def exampleuser_reviews():
    form = Reviews()
    return render_template("my_reviews.html", title='Reviews of example user', form=form)
>>>>>>> Login


@app.route("/findride", methods=['GET', 'POST'])
def findride():
    form = FindRideForm()
    if form.validate_on_submit():
        flash('You have been logged in successfully.', 'success')
    return render_template("findride.html", title="Find a ride", form=form)
