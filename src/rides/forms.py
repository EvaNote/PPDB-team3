from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from src.utils import user_access
from flask_babel import lazy_gettext
#
# class EditRideForm(FlaskForm):
#     first_name = StringField(lazy_gettext('First name'), validators=[DataRequired()])
#     last_name = StringField(lazy_gettext('Last name'), validators=[DataRequired()])
#     email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
#     password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), Length(min=8)])
#     confirm_password = PasswordField(lazy_gettext('Confirm password'), validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField(lazy_gettext('Sign up'))
#
#     def validate_email(self, email):  # j
#         if user_access.get_user_on_email(email.data):
#             raise ValidationError(lazy_gettext('The email is already registered.'))

class Filter_rides(FlaskForm):
    #TODO: validators?
    before = DateField(lazy_gettext("Before (yyyy-mm-dd)"))
    after = DateField(lazy_gettext("After (yyyy-mm-dd)"))
    submit = SubmitField(lazy_gettext('Filter'))