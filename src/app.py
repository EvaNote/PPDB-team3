from flask import Flask, render_template, url_for, flash, redirect
from config import config_data
from models import *
from forms import *


app = Flask(__name__)
app.config['SECRET_KEY'] = config_data['SECRET_KEY']
# connect to database
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
user_access = UserAccess(connection)


@app.route("/")
@app.route("/home")
def home():
    users = user_access.get_users()
    return render_template('home.html', users=users, loggedIn=False)

@app.route("/about")
def about():
    return render_template('about.html', title='About', loggedIn=False)

@app.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ', loggedIn=False)

@app.route("/contact")
def contact():
    return render_template('contact.html', title='contact', loggedIn=False)

@app.route("/account")
def account():
    return render_template('account.html', title='Account', loggedIn=True)

@app.route("/edit")
def account_edit():
    return render_template('account_edit.html', title='Edit account info', loggedIn=True)

@app.route("/myrides")
def myrides():
    return render_template('myrides.html', title='My rides', loggedIn=True)

@app.route("/user")
def user():
    return render_template('user.html', title='User profile', loggedIn=False)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # check if input is valid

    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}.', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form, loggedIn=False)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # check if input is valid
    if form.validate_on_submit():
        # TODO delete this login
        if form.email.data == 'admin@login.com' and form.password.data == 'admin':
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email and/or password.', 'danger')
    return render_template("login.html", title="Login", form=form, loggedIn=False)


@app.route("/newreview", methods=['GET', 'POST'])
def newreview():
    form = ReviewForm()
    return render_template('new_review.html', title='New review', form=form, loggedIn=True)


@app.route("/reviews", methods=['GET', 'POST'])
def reviews():
    form = Reviews()
    return render_template("my_reviews.html", title='My Reviews', form=form, loggedIn=True)


@app.route("/exampleuser/reviews", methods=['GET', 'POST'])
def exampleuser_reviews():
    form = Reviews()
    return render_template("my_reviews.html", title='Reviews of example user', form=form, loggedIn=True)

@app.route("/findride", methods=['GET', 'POST'])
def findride():
    form = FindRideForm()
    if form.validate_on_submit():
        flash('You have been logged in successfully.', 'success')
    return render_template("findride.html", title="Find a ride", form=form)


if __name__ == '__main__':
    app.run(debug=True)
