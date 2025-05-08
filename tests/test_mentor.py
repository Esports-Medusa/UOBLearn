import pytest
from app import app, db
from app.models import Student, Mentor, Meeting
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def student_and_mentor():
    student = Student(
        name='Nadiya',
        username='nadiya',
        email='nadiya@uob.edu',
        role='student',
        interests='AI,ML'
    )
    student.set_password('password')

    mentor = Mentor(
        name='Dr. Jiaqi',
        username='jiaqi',
        email='jiaqi@uob.edu',
        role='mentor',
        expertise='AI',
        available_hours='Mon 10:00-12:00',
        self_introduction='I love teaching'
    )
    mentor.set_password('password')

    db.session.add_all([student, mentor])
    db.session.commit()
    return student, mentor


def login_as(client, user):
    with client.session_transaction() as sess:
        sess['user_id'] = user.id
        sess['_user_id'] = user.id
        sess['role'] = user.role

def test_create_meeting_success(client, student_and_mentor):
    student, mentor = student_and_mentor
    login_as(client, student)

    response = client.post('/meeting/create', data={
        'mentor_id': mentor.id,
        'meeting_time': '2025-05-10T10:00:00',
        'description': 'Need help with Python project.'
    }, follow_redirects=True)

    assert b'Meeting request submitted successfully' in response.data
    meeting = Meeting.query.first()
    assert meeting is not None
    assert meeting.student_id == student.id
    assert meeting.mentor_id == mentor.id
    assert meeting.status == 'pending'

def test_create_meeting_fail_missing_fields(client, student_and_mentor):
    student, mentor = student_and_mentor
    login_as(client, student)

    response = client.post('/meeting/create', data={
        'mentor_id': mentor.id,
        'meeting_time': '2025-05-10T10:00:00'
        # Missing description
    }, follow_redirects=True)

    assert b'Error' in response.data
    assert Meeting.query.count() == 0

def test_non_student_cannot_create_meeting(client, student_and_mentor):
    student, mentor = student_and_mentor
    login_as(client, mentor)

    response = client.post('/meeting/create', data={
        'mentor_id': student.id,
        'meeting_time': '2025-05-10T10:00:00',
        'description': 'Invalid reverse booking'
    }, follow_redirects=True)

    assert b'Only students can create meetings' in response.data
