from flask import Blueprint, render_template, redirect, url_for, flash
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
            user = Student(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                interests=",".join(form.interests.data)
            )
            user.type = 'student'

        elif role == 'mentor':
            # 1. 将 time_slots 转为字符串列表
            time_slot_strs = []
            for slot_form in form.time_slots.entries:
                day = slot_form.form.day.data
                start = slot_form.form.start_time.data.strftime("%H:%M")
                end = slot_form.form.end_time.data.strftime("%H:%M")
                time_slot_strs.append(f"{day} {start}-{end}")

            user = Mentor(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                expertise=",".join(form.expertise.data),
                available_hours="; ".join(time_slot_strs),  # 存入 DB 的字段，字符串形式
                self_introduction=form.self_introduction.data
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
