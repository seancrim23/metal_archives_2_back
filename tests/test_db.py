import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    #db should return the same connection whenever its called with context
    with app.app_context():
        db = get_db()
        assert db is get_db()

    #without context it should be closed
    with pytest.raises(sqlite.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    #monkeypatch replaces real init db with a mock init db
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/user/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/user/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)