from flask import Flask
from src.config import config_data
from src.DBConnect import DBConnection
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# connect to database
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
app = Flask(__name__, instance_relative_config=False)
app.config['SECRET_KEY'] = config_data['SECRET_KEY']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
