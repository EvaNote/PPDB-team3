from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    msg = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Reviews(FlaskForm):
    submit_value = Markup('<b>Hello</b>')
    filter = SubmitField('<b>Hello</b>')
    search = StringField('')
