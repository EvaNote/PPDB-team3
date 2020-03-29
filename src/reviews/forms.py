from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length


class ReviewForm(FlaskForm):
    user_for = IntegerField('For')  # id of user
    user_from = IntegerField('From')  # id of user
    amount_of_stars = IntegerField('Rating', validators=[NumberRange(1, 5)])
    title = StringField('', validators=[DataRequired()])
    text = TextAreaField('', validators=[Length(0, 1000)])
    submit = SubmitField('Submit')


class Reviews(FlaskForm):
    submit_value = Markup('<b>Hello</b>')
    filter = SubmitField('<b>Hello</b>')
    search = StringField('')
