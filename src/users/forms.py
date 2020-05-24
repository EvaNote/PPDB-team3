from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from src.utils import user_access
from flask_babel import lazy_gettext


class RegistrationForm(FlaskForm):
    first_name = StringField(lazy_gettext('First name'), validators=[DataRequired()])
    last_name = StringField(lazy_gettext('Last name'), validators=[DataRequired()])
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(lazy_gettext('Confirm password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(lazy_gettext('Sign up'))

    def validate_email(self, email):  # j
        if user_access.get_user_on_email(email.data):
            raise ValidationError(lazy_gettext('The email is already registered.'))


class LoginForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember me'))
    submit = SubmitField(lazy_gettext('Log in'))


class DeleteUserForm(FlaskForm):
    delete = SubmitField(lazy_gettext('Delete account'))


class VehicleForm(FlaskForm):
    brand = StringField(lazy_gettext('Brand'), validators=[DataRequired()])
    model = StringField(lazy_gettext('Model'), validators=[DataRequired()])
    color = StringField(lazy_gettext('Color'))
    plateNumber = StringField(lazy_gettext('Plate number'), validators=[DataRequired()])
    seats = IntegerField(lazy_gettext('Seats'), validators=[InputRequired()])
    constructionYear = IntegerField(lazy_gettext('Construction Year'),[validators.optional()])
    consumption = StringField(lazy_gettext('Fuel Consumption'))
    fuelType = SelectField(lazy_gettext('Fuel type'), choices=[('benzine', lazy_gettext('Gasoline/Petrol/Benzine')), ('diesel', lazy_gettext('Diesel')),
                                                ('LPG', lazy_gettext('Liquified Petroleum')), ('electricity', lazy_gettext('Electricity')),
                                                ('CNG', lazy_gettext('Compressed Natural Gas')),
                                                ('ethanol', lazy_gettext('Ethanol')), ('bio-diesel', lazy_gettext('Bio-diesel'))])
    picture = FileField(lazy_gettext('Upload car picture'), validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField(lazy_gettext('Register vehicle'))


class EditAccountForm(FlaskForm):
    first_name = StringField(lazy_gettext('First name'), validators=[DataRequired()])
    last_name = StringField(lazy_gettext('Last name'), validators=[DataRequired()])
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    gender = SelectField(lazy_gettext('Gender'), choices=[('M',lazy_gettext('Male')),('F', lazy_gettext('Female')), (None, lazy_gettext('Other'))])
    age = IntegerField(lazy_gettext('Age'),[validators.optional()])
    phone_number = StringField(lazy_gettext('Phone number'))
    picture = FileField(lazy_gettext('Upload profile picture'), validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField(lazy_gettext('Save'))
    delete = SubmitField(lazy_gettext('Delete account'))


class EditAddressForm(FlaskForm):
    street = StringField(lazy_gettext('Street'), validators=[DataRequired()])
    nr = StringField(lazy_gettext('Number'), validators=[DataRequired()])
    city = StringField(lazy_gettext('City'), validators=[DataRequired()])
    postal_code = StringField(lazy_gettext('Postal code'), validators=[DataRequired()])

    submit = SubmitField(lazy_gettext('Save'))


class SelectSubject(FlaskForm):
    subject = SelectField(lazy_gettext('Subject'), choices=[('Lost item',lazy_gettext('Lost item')),('Empty',lazy_gettext('Empty'))])
    submit = SubmitField(lazy_gettext('Make Form'))


class getCalendar(FlaskForm):
    submit = SubmitField(lazy_gettext('Calendar'))