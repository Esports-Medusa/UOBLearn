from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Course

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
    if current_user.role == 'admin' and request.method == 'POST':
        # 处理课程添加表单
        title = request.form.get('title')
        platform = request.form.get('platform')
        difficulty = request.form.get('difficulty')
        subject = request.form.get('subject')
        url = request.form.get('url')

        if title and platform and difficulty and subject and url:
            course = Course(title=title, platform=platform, difficulty=difficulty, subject=subject, url=url)
            db.session.add(course)
            db.session.commit()
            flash("New course added successfully!", "success")
        else:
            flash("Please fill out all fields.", "danger")

    return render_template('profile.html', user=current_user)


#saving courses
@bp.route('/save_course/<int:course_id>', methods=['POST'])
@login_required
def save_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.saved_courses:
        current_user.saved_courses.append(course)
        db.session.commit()
        flash('Course saved successfully!', 'success')
    else:
        flash('Course already saved.', 'info')
    return redirect(url_for('course_detail', course_id=course.id))
