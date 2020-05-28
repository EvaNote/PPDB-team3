from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from src.utils import user_access
from flask_babel import lazy_gettext


class Filter_rides(FlaskForm):
    before = DateField(lazy_gettext("Before (yyyy-mm-dd)"))
    after = DateField(lazy_gettext("After (yyyy-mm-dd)"))
    submit = SubmitField(lazy_gettext('Show results'))
    reset = SubmitField()
