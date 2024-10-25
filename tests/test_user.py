#update accordingly from tutorial boilerplate
import pytest
from flask import g, session
from flaskr.db import get_db

def test_create_user(client, app):
    #dont need this bc we have no get for user/create
    #assert client.get('/user/create').status_code == 200
    response = client.post(
        '/user/create', data={'username': 'a', 'password': 'a'}
    )
    #assert that status code is 200 successful create
    
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_create_user_validate_input(client, username, password, message):
    response = client.post(
        '/user/create',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    response = auth.login()
    #assert code 200?

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect username or password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

