from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired
from app.models import Mentor

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')


class MentorForm(FlaskForm):

    mentor_name = SelectField('Mentor Name',coerce=int, validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    message = TextAreaField('Message ', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(MentorForm, self).__init__(*args, **kwargs)
        # Populate mentor names from the database
        mentors = Mentor.query.all()
        self.mentor_name.choices = [(mentor.id, mentor.name) for mentor in mentors]