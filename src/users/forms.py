from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.utils import user_access


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):  # j
        if user_access.get_user(email.data):
            raise ValidationError('The email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class VehicleForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    plateNumber = StringField('Plate number', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    manufacturingDate = DateField('Manufacturing Date', format='%d-%m-%y')
    mileage = StringField('Mileage', validators=[DataRequired()])
    fuelType = SelectField('fuelType', choices=[('Gasoline', 'Gasoline'), ('Diesel', 'Diesel'),
                                                ('Liquified Petroleum', 'Liquified Petroleum'),
                                                ('Compressed Natural Gas', 'Compressed Natural Gas'),
                                                ('Ethanol', 'Ethanol'), ('Bio-diesel', 'Bio-diesel')])
    submit = SubmitField('Register vehicle')
