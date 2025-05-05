from flask import Blueprint, render_template, request
from app.models import Course
from flask_login import current_user

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/')
def course_list():
    search_query = request.args.get('search', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 9

    query = Course.query.filter(Course.title.ilike(f"%{search_query}%"))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # 预先计算页码范围（中心±2）
    start_page = max(pagination.page - 2, 1)
    end_page = min(pagination.page + 2, pagination.pages)
    page_range = list(range(start_page, end_page + 1))

    return render_template(
        'courses.html',
        courses=pagination,
        search=search_query,
        page_range=page_range,
        current_user=current_user
    )


