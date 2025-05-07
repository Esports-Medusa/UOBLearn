import pytest

def test_unauthenticated_user_saves_course(client):
    response = client.get("/saved_courses/add/1/saved", follow_redirects=True)

    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data


def test_saved_courses_requires_login(client):

    response = client.get("/saved_courses/", follow_redirects=True)

    # Check that the login page appears in the redirected response
    assert b"Please log in to access this page." in response.data