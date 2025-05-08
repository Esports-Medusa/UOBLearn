import pytest
from app import app, db
from app.models import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Added fake users to the database for testing login
            test_user = User(
                name="Test User",
                username="testuser1",
                email="testuser1@uob.edu",
                role="student",
                type="student"
            )

            test_user.set_password("testpassword")
            db.session.add(test_user)
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()

# Positive login test
def test_login_valid(client):
    response = client.post("/auth/login", data={
        "email": "testuser1@uob.edu",
        "password": "testpassword"
    }, follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/profile" in response.headers.get("Location", "")

# Negative login test
def test_login_invalid(client):
    response = client.post("/auth/login", data={
        "email": "wrongemail@uob.edu",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data
