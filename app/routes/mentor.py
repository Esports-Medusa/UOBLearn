from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Mentor
from app.forms import MentorForm

bp = Blueprint('mentors', __name__, url_prefix='/mentors')

# 示例：导师主页
@bp.route('/', methods=['GET', 'POST'])
def mentor_home():
    q = db.select(Mentor)
    mentors = db.session.scalars(q).all()
    # return redirect(url_for('product', id=int(form.choice.data)))

    form = MentorForm()
    if form.validate_on_submit():
        mentor_id = form.mentor_name.data  # Get the mentor ID from the form submission
        flash(f'Appointment booked with mentor ID: {mentor_id}')

    return render_template('mentors.html', title="Mentors", mentors=mentors, form=form)


# 示例：导师接受预约
@bp.route('/appointments')
def view_appointments():

    return "View mentorship requests (Placeholder)"

# 示例：导师信息修改
@bp.route('/profile')
def edit_profile():
    return "Mentor profile editor (Placeholder)"
