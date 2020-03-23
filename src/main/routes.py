from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    users = None  # user_access.get_users()
    return render_template('home.html', users=users, loggedIn=False)


@main.route("/about")
def about():
    return render_template('about.html', title='About', loggedIn=False)


@main.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ', loggedIn=False)


@main.route("/contact")
def contact():
    return render_template('contact.html', title='contact', loggedIn=False)
