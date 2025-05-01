from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import ChooseForm
from app.models import User, Course, Notification

bp = Blueprint('auth', __name__, url_prefix='/auth')


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


# register page
@bp.route('/register')
def register():
    return render_template('register.html')


# logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# User Profile Page
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    notifications = []

    if current_user.role == 'student':
        notifications = Notification.query.filter_by(
            user_id=current_user.id
        ).order_by(Notification.timestamp.desc()).all()

    if current_user.role == 'admin' and request.method == 'POST':
        # Handle course addition form
        title = request.form.get('title')
        platform = request.form.get('platform')
        difficulty = request.form.get('difficulty')
        subject = request.form.get('subject')
        url = request.form.get('url')

        if title and platform and difficulty and subject and url:
            # 添加课程
            course = Course(
                title=title,
                platform=platform,
                difficulty=difficulty,
                subject=subject,
                url=url
            )
            db.session.add(course)
            db.session.commit()

            # ========== Observer Pattern: send notification ==========
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
            # ==============================================

            flash("New course added successfully!", category="success")
        else:
            flash("Please fill out all fields.", category="danger")

    return render_template('profile.html', user=current_user, notifications=notifications)

#course recommendations
@bp.route('/courses')
def all_courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@bp.route('/saved_courses', methods=['GET', 'POST'])
@login_required
def saved_courses_display():
    form = ChooseForm()

    if form.validate_on_submit():
        remove_course = Course.query.get(form.choice.data)  # Get the course from the form choice
        if remove_course and remove_course in current_user.saved_courses:
            # Remove the course from the saved list
            current_user.saved_courses.remove(remove_course)
            db.session.commit()
            flash(f'{remove_course.title} removed from your saved list.', 'success')
        else:
            flash('Course not found in your saved list.', 'danger')

        return redirect(url_for('saved_courses_display'))
    
    # Fetch the user's saved courses to display
    saved_courses = current_user.saved_courses
    return render_template('saved_courses.html', saved_courses=saved_courses, form=form)


@bp.route('/save_course/<int:course_id>', methods=['POST'])
@login_required
def save_course(course_id):
    course = Course.query.get_or_404(course_id)

    if course in current_user.saved_courses:
        # Unsave course if already saved
        current_user.saved_courses.remove(course)
        flash(f'{course.title} removed from your saved courses.', 'info')
    else:
        current_user.saved_courses.append(course)
        flash(f'{course.title} saved to your courses!', 'success')

    db.session.commit()

    return redirect(url_for('saved_courses_display'))  # Redirect back to the saved courses page
