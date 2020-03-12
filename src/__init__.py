from flask import Flask
from src.config import config_data
from src.models import *
import os

# connect to database
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
user_access = UserAccess(connection)
app = Flask(__name__, instance_relative_config=False)
app.config['SECRET_KEY'] = config_data['SECRET_KEY']

