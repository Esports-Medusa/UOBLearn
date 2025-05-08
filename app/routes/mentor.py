from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Mentor
from app import db
from flask_login import current_user


bp = Blueprint('mentor', __name__, url_prefix='/mentor')

@bp.route('/')
def mentor_list():
    search_query = request.args.get('search', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 9

    query = Mentor.query.filter(Mentor.name.ilike(f"%{search_query}%"))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('mentor.html', mentors=pagination, search=search_query, current_user=current_user)


# Example: Mentor responds to meeting request
@bp.route('/appointments')
def view_appointments():
    return "View mentorship requests (Placeholder)"

# Example: Edit mentor information
@bp.route('/profile')
def edit_profile():
    return "Mentor profile editor (Placeholder)"

