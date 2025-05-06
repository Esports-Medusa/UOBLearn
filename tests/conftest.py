import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # optional: disable CSRF protection in tests
    with app.test_client() as client:
        yield client
