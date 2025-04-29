from flask import Blueprint, render_template
from app.models import Course


bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/')
def index():
    return "Courses Home"
