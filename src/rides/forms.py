from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext


class FindRideForm(FlaskForm):
    fromField = StringField(lazy_gettext('From'), validators=[DataRequired()])
    toField = StringField(lazy_gettext('To'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Search'))
