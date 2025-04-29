from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')


class MentorForm(FlaskForm):

    mentor_name = SelectField('Mentor Name', validators=[DataRequired()], choices=['Jane', 'Alex', 'Sanjay','Maria','Liam'])
    topic = StringField('Topic', validators=[DataRequired()])
    message = TextAreaField('Message ', validators=[DataRequired()])
    submit = SubmitField('Submit')