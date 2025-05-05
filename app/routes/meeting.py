from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import Meeting, db
from datetime import datetime

bp = Blueprint('meeting', __name__, url_prefix='/meeting')

@bp.route('/', methods=['GET'])
@login_required
def meeting_page():
    if current_user.role == 'student':
        meetings = Meeting.query.filter_by(student_id=current_user.id).order_by(Meeting.created_at.desc()).all()

        # Mark all responded appointments as viewed
        unread_updated = False
        for m in meetings:
            if m.status in ['accepted', 'rejected'] and not m.is_viewed_by_student:
                m.is_viewed_by_student = True
                unread_updated = True

        if unread_updated:
            db.session.commit()

        return render_template('meeting.html', meetings=meetings, is_student=True)

    elif current_user.role == 'mentor':
        meetings = Meeting.query.filter_by(mentor_id=current_user.id).order_by(Meeting.created_at.desc()).all()
        return render_template('meeting.html', meetings=meetings, is_student=False)

    else:
        flash("You do not have permission to access the appointment page.")
        return redirect(url_for('mentor.mentor_list'))

@bp.route('/respond/<int:meeting_id>', methods=['POST'])
@login_required
def respond_to_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)

    if current_user.id != meeting.mentor_id:
        flash("You do not have permission to modify this appointment.")
        return redirect(url_for('meeting.meeting_page'))

    status = request.form.get('status')
    message = request.form.get('response_message')

    if status not in ['accepted', 'rejected']:
        flash("Invalid status")
        return redirect(url_for('meeting.meeting_page'))

    meeting.status = status
    meeting.response_message = message
    meeting.is_viewed_by_student = False  # Ensure student sees updated status
    db.session.commit()
    flash("Appointment status has been updated.")
    return redirect(url_for('meeting.meeting_page'))


@bp.route('/create', methods=['POST'])
@login_required
def create_meeting():
    if current_user.role != 'student':
        flash("Only students can create meetings.")
        return redirect(url_for('mentor.mentor_list'))

    mentor_id = request.form.get('mentor_id')
    meeting_time = request.form.get('meeting_time')
    description = request.form.get('description')

    try:
        new_meeting = Meeting(
            student_id=current_user.id,
            mentor_id=int(mentor_id),
            meeting_time=datetime.fromisoformat(meeting_time),
            description=description
        )
        db.session.add(new_meeting)
        db.session.commit()
        flash("Meeting request submitted successfully.")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}")

    return redirect(url_for('mentor.mentor_list'))
