from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext


class FindRideForm(FlaskForm):
    fromField = StringField(lazy_gettext('From'), validators=[DataRequired()])
    toField = StringField(lazy_gettext('To'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Search'))

class CreateRideForm(FlaskForm):
    fromField = StringField('From', validators=[DataRequired()])
    toField = StringField('To', validators=[DataRequired()])

    Date = DateField('Date (dd/mm/yy)', format='%d/%m/%Y')
    Time = TimeField('Time', validators=[DataRequired()])

    submit = SubmitField('Create')
