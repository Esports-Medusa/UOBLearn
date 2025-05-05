from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import SavedCourse, Course

bp = Blueprint('saved_courses_bp', __name__, url_prefix='/saved_courses')

# add to saved/favourite
@bp.route("/add/<int:course_id>/<string:type>")
@login_required
def save_course(course_id, type):
    if type not in ["saved", "favourite"]:
        flash("Invalid save type", "danger")
        return redirect(url_for("home"))

    existing = SavedCourse.query.filter_by(user_id=current_user.id, course_id=course_id, type=type).first()
    if not existing:
        saved = SavedCourse(user_id=current_user.id, course_id=course_id, type=type)
        db.session.add(saved)
        db.session.commit()
        flash(f"Course {type} successfully!", "success")
    else:
        flash(f"You already {type}d this course.", "info")

    return redirect(request.referrer or url_for("home"))

# remove save/fav
@bp.route("/remove/<int:course_id>/<string:type>")
@login_required
def remove_course(course_id, type):
    saved = SavedCourse.query.filter_by(user_id=current_user.id, course_id=course_id, type=type).first()
    if saved:
        db.session.delete(saved)
        db.session.commit()
        flash(f"Course removed from {type}s.", "success")
    else:
        flash("Course not found.", "danger")
    return redirect(request.referrer or url_for("saved_courses_bp.saved_courses"))


@bp.route("/")
@login_required
def saved_courses():
    saved = [s.course for s in current_user.saved_courses if s.type == "saved"]
    favourites = [s.course for s in current_user.saved_courses if s.type == "favourite"]
    return render_template("saved_courses.html", saved=saved, favourites=favourites)
