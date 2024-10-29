import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/new', methods=('POST',))
def create_user():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    
    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return redirect(url_for("user.login"))

    flash(error)

@bp.route('/login', methods=('POST',))
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username or password.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect username or password.'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return redirect(url_for('index'))

    flash(error)

@bp.route('/<int:id>', methods=('GET',))
def get_one_user(id):
    band = get_band(id)
    return band

def get_user(id):
    #refactor to not include password in query results
    user = get_db().execute(
        'SELECT username FROM user WHERE id = ?',
        (id,)
    ).fetchone()

    if band is None:
        abort(404, f"User id {id} doesn't exist.")
    
    return band

@bp.route('/<int:id>/update', methods=('POST',))
def update(id):
    user = get_user(id)

    #build out as band object expands
    #has to be a better way to do this to be more dynamic
    name = request.form['name']
    error = None

    if not name:
        error = 'Name is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'UPDATE user SET name = ? WHERE id = ?',
            (name, id)
        )
        db.commit()
        return redirect(url_for('index'))


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(for_url('index'))

#TODO - modifications by user
@bp.route('/<int:id>/modifications', methods=('GET',))
def get_modifications(id):
    return redirect(for_url('index'))

#TODO - reviews by user
@bp.route('/<int:id>/reviews', methods=('GET',))
def get_reviews(id):
    return redirect(for_url('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view    