from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user
from app import db
from app.forms import RegistrationForm
from app.models import Student, Mentor

bp = Blueprint('register', __name__, url_prefix='/register')


@bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        role = form.role.data
        if role == 'student':
            interests_list = form.interests.data
            user = Student(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                interests=",".join(interests_list)
            )
            user.type = 'student'

        elif role == 'mentor':
            expertise_list = form.expertise.data
            time_slots = []
            for slot in form.time_slots.entries:
                day = slot.form.day.data
                start = slot.form.start_time.data.strftime('%H:%M')
                end = slot.form.end_time.data.strftime('%H:%M')
                time_slots.append(f"{day} {start}-{end}")
            user = Mentor(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                expertise=",".join(expertise_list),
                self_introduction=form.self_introduction.data,
                available_hours="; ".join(time_slots)
            )
            user.type = 'mentor'
        else:
            flash("Invalid role selected.")
            return redirect(url_for('register.register'))

        user.role = role

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Registration successful! Welcome!')
        return redirect(url_for('auth.profile'))

    return render_template('register.html', form=form)
