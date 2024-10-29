from flask import (
    Blueprint, flash, g, redirect, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.user import login_required
from flaskr.db import get_db

bp = Blueprint('track', __name__, url_prefix='/track')

#CREATE READ UPDATE DELETE

@bp.route('/create', methods=('POST',))
def create():
    #get release id from the session / context ?
    #get user id from session / context?
    name = request.form['name']
    error = None

    if not name:
        error = 'Name is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO tracks (name) VALUES (?)',
            (name)
        )
        db.commit()
        return redirect(url_for('index'))

@bp.route('/<int:id>', methods=('GET',))
def get_one_track(id):
    track = get_track(id)
    return track

#at some point we'll need a get all bands by a user function 
#but get band by id is fine for now
def get_track(id):
    track = get_db().execute(
        'SELECT * FROM tracks WHERE id = ?',
        (id,)
    ).fetchone()

    if track is None:
        abort(404, f"Track id {id} doesn't exist.")
    
    return track

@bp.route('/<int:id>/update', methods=('POST',))
@login_required
def update(id):
    track = get_track(id)

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
            'UPDATE tracks SET name = ? WHERE id = ?',
            (name, id)
        )
        db.commit()
        return redirect(url_for('index'))


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_track(id)
    db = get_db()
    db.execute('DELETE FROM tracks WHERE id = ?', (id,))
    db.commit()
    return redirect(for_url('index'))