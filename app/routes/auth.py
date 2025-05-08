from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Course, Notification
from app.notification import NotificationCenter
from app.forms import StudentProfileEditForm, MentorProfileEditForm


bp = Blueprint('auth', __name__, url_prefix='/auth')
notification_center = NotificationCenter()


# login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('auth.profile'))

    return render_template('login.html')


# logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    notifications = []
    student_form = None
    mentor_form = None

    if current_user.role == 'student':
        student_form = StudentProfileEditForm(obj=current_user)

        # Display interests as a list
        student_form.interests.data = current_user.interests.split(',') if current_user.interests else []

        if student_form.validate_on_submit():
            current_user.username = student_form.username.data
            current_user.interests = ",".join(student_form.interests.data)
            db.session.commit()
            flash("Profile updated!", "success")
            return redirect(url_for('auth.profile'))

        # Student notification list
        notifications = Notification.query.filter_by(
            user_id=current_user.id
        ).order_by(Notification.timestamp.desc()).all()

    elif current_user.role == 'mentor':
        mentor_form = MentorProfileEditForm()

        if request.method == 'GET':
            mentor_form.username.data = current_user.username
            mentor_form.expertise.data = current_user.expertise.split(',') if current_user.expertise else []
            mentor_form.self_introduction.data = current_user.self_introduction

            # Parse time_slots string into field objects
            mentor_form.time_slots.entries.clear()
            if current_user.available_hours:
                for slot in current_user.available_hours.split('; '):
                    try:
                        day, times = slot.split(' ')
                        start, end = times.split('-')

                        # Convert to datetime.time type
                        start_time = datetime.strptime(start, "%H:%M").time()
                        end_time = datetime.strptime(end, "%H:%M").time()

                        mentor_form.time_slots.append_entry({
                            'day': day,
                            'start_time': start_time,
                            'end_time': end_time
                        })
                    except Exception as e:
                        print("TimeSlot parse error:", e)
                        continue

        elif mentor_form.validate_on_submit():
            current_user.username = mentor_form.username.data
            current_user.expertise = ",".join(mentor_form.expertise.data)
            current_user.self_introduction = mentor_form.self_introduction.data

            # Convert time_slots back to string for database storage
            time_slot_strs = []
            for slot_form in mentor_form.time_slots.entries:
                day = slot_form.form.day.data
                start = slot_form.form.start_time.data.strftime("%H:%M")
                end = slot_form.form.end_time.data.strftime("%H:%M")
                time_slot_strs.append(f"{day} {start}-{end}")

            current_user.available_hours = "; ".join(time_slot_strs)

            db.session.commit()
            flash("Profile updated!", "success")
            return redirect(url_for('auth.profile'))

    # ============ Logic for admin to add courses ============
    if current_user.role == 'admin' and request.method == 'POST':
        title = request.form.get('title')
        platform = request.form.get('platform')
        difficulty = request.form.get('difficulty')
        subject = request.form.get('subject')
        url = request.form.get('url')

        if title and platform and difficulty and subject and url:
            new_course = Course(
                title=title,
                platform=platform,
                difficulty=difficulty,
                subject=subject,
                url=url
            )
            db.session.add(new_course)
            db.session.commit()

            # Logic to send notifications to students（Observer Pattern）
            from app.observers import Subject
            from app.concrete_observers import StudentObserver
            from app.models import User

            subject_center = Subject()
            all_students = User.query.filter_by(role="student").all()
            for student in all_students:
                observer = StudentObserver(student)
                subject_center.attach(observer)

            message = f"📢 New course added: \"{title}\" (Subject: {subject})\nLearn more at: {url}"
            subject_center.notify(message)

            db.session.commit()
            flash("New course added successfully!", category="success")
        else:
            flash("Please fill out all fields.", category="danger")

    return render_template(
        'profile.html',
        user=current_user,
        notifications=notifications,
        student_form=student_form,
        mentor_form=mentor_form
    )



