from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.sql.operators import from_

from app import db
from app.models import Mentor, Appointment
from app.forms import MentorForm
from datetime import datetime

bp = Blueprint('mentors', __name__, url_prefix='/mentors')

# 示例：导师主页
@bp.route('/', methods=['GET', 'POST'])
def mentor_home():

    q = db.select(Mentor)
    mentors = db.session.scalars(q).all()
    # return redirect(url_for('product', id=int(form.choice.data)))
    form = MentorForm()

    if form.validate_on_submit():
        mentor_id = form.mentor_name.data  # This is an integer
        mentor = Mentor.query.get(mentor_id)
        if mentor:
            flash(f'Appointment requested with mentor: {mentor.name}', 'success')



        new_appointment = Appointment(mentor_name=mentor.name, topic=form.topic.data,  message=form. message.data )
        db.session.add(new_appointment)
        db.session.commit()

    return render_template('mentor.html', title="Mentors", mentors=mentors, form=form)


# 示例：导师接受预约
@bp.route('/appointments')
def view_appointments():

    return "View mentorship requests (Placeholder)"

# 示例：导师信息修改
@bp.route('/profile')
def edit_profile():
    return "Mentor profile editor (Placeholder)"
