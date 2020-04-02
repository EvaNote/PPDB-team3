from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
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
            raise ValidationError('email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class VehicleForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    color = StringField('Color')
    plateNumber = StringField('Plate number', validators=[DataRequired()])
    seats = IntegerField('Seats', validators=[InputRequired()])
    constructionYear = IntegerField('Construction Year',[validators.optional()])
    consumption = StringField('Fuel Consumption')
    fuelType = SelectField('fuelType', choices=[('benzine', 'Gasoline/Petrol/Benzine'), ('diesel', 'Diesel'),
                                                ('LPG', 'Liquified Petroleum'), ('electricity', 'Electricity'),
                                                ('CNG', 'Compressed Natural Gas'),
                                                ('ethanol', 'Ethanol'), ('bio-diesel', 'Bio-diesel')])
    submit = SubmitField('Register vehicle')

class EditAccountForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[('M','Male'),('F', 'Female'), (None, 'Other')])
    age = IntegerField('Age',[validators.optional()])
    phone_number = StringField('Phone number')

    submit = SubmitField('Save')

class EditAddressForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()])
    nr = StringField('Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = IntegerField('Postal code')
    country = StringField('Country', validators=[DataRequired()])

    submit = SubmitField('Save')
