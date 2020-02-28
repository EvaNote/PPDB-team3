from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from config import config_data
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = config_data['SECRET_KEY']
# connect to database
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
user_access = UserAccess(connection)

@app.route("/")
@app.route("/home")
def home():
    users = user_access.get_users()
    return render_template('home.html', users=users)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/account")
def account():
    return render_template('account.html', title='Account')

@app.route("/account/edit")
def editaccount():
    return render_template('editaccount.html', title='Edit account info')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # check if input is valid

    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}.', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


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
    return render_template("login.html", title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)