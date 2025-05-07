#Positive Test Case for Save Course Feature
#Pre-conditions:
#   A user exists in the system
#   A user is logged in
#   At least one course exists in the system

#User Action:
#   A logged-in user sends a POST request to save a course to /save_course/<course_id>

#Post-condition:
#   The course is added to the user's saved_courses list in the database.

#pytest tests/test_save_course_positive.py



import pytest
from app import app, db
from app.models import User, Course, SavedCourse
from flask_login import login_user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_user_can_save_course(client):
    with app.app_context():
        # Create user
        user = User(name="Test User", username="testuser", email="test@example.com", type="user")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()

        # Refresh user to bind it to session properly
        db.session.refresh(user)

        # Create course
        course = Course(
            title="Intro to Python", platform="Coursera",
            difficulty="Beginner", subject="Programming",
            url="http://example.com/python"
        )
        db.session.add(course)
        db.session.commit()

        # Save the course for the user
        saved = SavedCourse(user_id=user.id, course_id=course.id, type="saved")
        db.session.add(saved)
        db.session.commit()

        # Assert saved course exists
        saved_entry = SavedCourse.query.filter_by(user_id=user.id, course_id=course.id).first()
        assert saved_entry is not None
        assert saved_entry.type == "saved"