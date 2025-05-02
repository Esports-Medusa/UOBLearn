import pytest
from app import app, db
from app.models import Student, Course
from flask_login import login_user

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
        student1 = Student(
            username="student1",
            email="student1@uob.edu",
            role="student",
            type="student",
            interests="AI, ML, Cloud"
        )
        student1.set_password('password1')  # Set the password for the student
        db.session.add(student1)

        student2 = Student(
            username="student2",
            email="student2@uob.edu",
            role="student",
            type="student",
            interests="AI, ML, Cloud"
        )
        student2.set_password('password2')  # Set the password for the student
        db.session.add(student2)

        course1 = Course(
            title='Introduction to Blockchain 1',
            platform='edX',
            difficulty='Intermediate',
            subject='Blockchain',
            url= 'https://www.edx.org/course/introduction-to-blockchain-1'
            )
        db.session.add(course1)

        course2 = Course(
            title='Introduction to Blockchain 2',
            platform='Udemy',
            difficulty='Intermediate',
            subject='Cybersecurity',
            url= 'https://www.udemy.com/course/introduction-to-cybersecurity-2'
            )
        db.session.add(course2)
        db.session.commit()

        return student1, student2, course1, course2

def test_multiple_students_can_save_multiple_courses(test_client, setup_data):
    student1, student2, course1, course2 = setup_data  # Get students and courses from the fixture

    # Log in as student1 and save the first course
    test_client.post('/login', data=dict(username='student1', password='password1'))
    response = test_client.post(f'/save_course/{course1.id}', follow_redirects=True)

    # Assert that student1 has saved the first course
    student1 = Student.query.get(student1.id)
    assert course1 in student1.saved_courses, 'Student 1 should have saved the first course'

    # Save the second course for student1
    response = test_client.post(f'/save_course/{course2.id}', follow_redirects=True)

    # Assert that student1 has saved the second course as well
    student1 = Student.query.get(student1.id)
    assert course2 in student1.saved_courses, 'Student 1 should have saved the second course'

    test_client.post('/login', data=dict(username='student2', password='password2'))
    response = test_client.post(f'/save_course/{course1.id}', follow_redirects=True)
    student2 = Student.query.get(student2.id)
    assert course1 in student2.saved_courses, 'Student 2 should have saved the first course'

    response = test_client.post(f'/save_course/{course2.id}', follow_redirects=True)
    student2 = Student.query.get(student2.id)
    assert course2 in student2.saved_courses, 'Student 2 should have saved the second course'

    # Verify that both students now have both courses saved
    assert course1 in student1.saved_courses, 'Ensure student1 saved both courses'
    assert course2 in student1.saved_courses

    assert course1 in student2.saved_courses, 'Ensure student2 saved both courses'
    assert course2 in student2.saved_courses

def test_student_can_remove_course(test_client, setup_data):
    student1, student2, course1, course2 = setup_data

    # Log in as student1 and remove a saved course1
    test_client.post('/login', data=dict(username='student1', password='password1'))
    test_client.post(f'/save_course/{course1.id}', follow_redirects=True)

    response = test_client.post(f'/save_course/{course1.id}', follow_redirects=True)  # Simulate clicking 'remove'

    # Assert that the course was removed from saved courses
    student1 = Student.query.get(student1.id)
    assert course1 not in student1.saved_courses, 'Student 1 should have only course2 saved'

    # Log in as student2 and ensure student2 still has the course saved
    test_client.post('/login', data=dict(username='student2', password='password2'))
    student2 = Student.query.get(student2.id)
    assert course1 in student2.saved_courses, 'Student 2 should have both tests saved'

#Demonnstrate a user can save multiple courses and a course can be saved
#by multiple users
# saved courses can be removed by a user without affecting another
#For this function to work the user must be logged in and their role must be as a student