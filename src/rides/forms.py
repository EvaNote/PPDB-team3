from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FindRideForm(FlaskForm):
    fromField = StringField('From', validators=[DataRequired()])
    toField = StringField('To', validators=[DataRequired()])
    submit = SubmitField('Search')
