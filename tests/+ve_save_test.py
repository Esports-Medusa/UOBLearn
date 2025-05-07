#Positive Test Case for Save Course Feature
#Pre-conditions:
#   A user exists in the system
#   A user is logged in
#   At least one course exists in the system

#User Action:
#   A logged-in user sends a POST request to save a course to /save_course/<course_id>

#Post-condition:
#   The course is added to the user's saved_courses list in the database.


import pytest
from app import app, db
from app.models import User, Course

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def setup_data():
    with app.app_context():
        test_subject1 = User(
            username="test_subject1",
            email="testsubject1@uob.edu",
            role="student",
            type="student",
            interests="AI, Cloud"
        )
        test_subject1.set_password('test_password1')
        db.session.add(test_subject1)

        test_course1 = Course(
            title='Test Course 1',
            platform='TestPlatf',
            difficulty='Intermediate',
            subject='Test',
            url= 'https://www.test.org/test_course_1'
            )
        db.session.add(test_course1)
        db.session.commit()

        return test_subject1, test_course1

def test_logged_in_user_saves_course(test_client, setup_data):
    test_subject1, test_course1 = setup_data  # Get test data from the fixture

    # User logs in and saves the first course
    test_client.post('/login', data=dict(username='test_subject1', password='test_password1'))
    response = test_client.post(f'/save_course/{test_course1.id}', follow_redirects=True)

    # Assert that the user has saved the first course
    test_subject1 = User.query.get(test_subject1.id)
    assert test_course1 in test_subject1.saved_courses, 'User should have saved the course'

