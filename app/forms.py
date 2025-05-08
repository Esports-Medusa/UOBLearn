from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectMultipleField,
    SelectField, SubmitField, FieldList, FormField, TimeField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import Form as NoCsrfForm  # Nested fields don't need CSRF

# choices
INTEREST_CHOICES = [('AI', 'AI'), ('ML', 'ML'), ('Cloud', 'Cloud'), ('Cybersecurity', 'Cybersecurity')]
WEEKDAYS = [('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday')]

# time slot form
class TimeSlotForm(NoCsrfForm):
    day = SelectField('Day', choices=WEEKDAYS, validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    # common
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')])

    # role
    role = SelectField('Register as', choices=[('student', 'Student'), ('mentor', 'Mentor')],
                       validators=[DataRequired()])

    # student
    interests = SelectMultipleField(
        'Select your interests',
        choices=INTEREST_CHOICES,
        validators=[DataRequired()]
    )

    # mentor
    expertise = SelectMultipleField(
        'Expertise',
        choices=INTEREST_CHOICES,
        validators=[DataRequired()]
    )
    self_introduction = TextAreaField('Self Introduction', validators=[Length(min=10)])
    time_slots = FieldList(FormField(TimeSlotForm), min_entries=1, max_entries=10)

    submit = SubmitField('Register')

    # Make the changes inside the validate method of RegistrationForm.
    def validate(self, **kwargs):
        role = self.role.data

        if role == 'student':
            # Clear mentor field data and validation
            self.expertise.data = []
            self.self_introduction.data = None
            self.time_slots.entries = []  # Clear entries to avoid empty data

            # Remove validators
            self.expertise.validators = []
            self.self_introduction.validators = []
            self.time_slots.validators = []

        elif role == 'mentor':
            # Clear data from student-specific fields
            self.interests.data = []
            self.interests.validators = []

        return super().validate(**kwargs)


# student change form
class StudentProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    interests = SelectMultipleField(
        'Select your interests',
        choices=INTEREST_CHOICES,
        validators=[DataRequired()]
    )
    submit = SubmitField('Update')


# mentor change form
class MentorProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    expertise = SelectMultipleField(
        'Expertise',
        choices=INTEREST_CHOICES,
        validators=[DataRequired()]
    )
    self_introduction = TextAreaField('Self Introduction', validators=[Length(min=10)])
    time_slots = FieldList(FormField(TimeSlotForm), min_entries=1, max_entries=10)
    submit = SubmitField('Update')
