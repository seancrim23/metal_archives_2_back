from flask import (
    Blueprint, flash, g, redirect, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.user import login_required
from flaskr.db import get_db

bp = Blueprint('release', __name__, url_prefix='/release')

@bp.route('/create', methods=('POST',))
def create():
    #get band id from the session / context ?
    name = request.form['name']
    error = None

    if not name:
        error = 'Name is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO band (name) VALUES (?)',
            (name)
        )
        db.commit()
        return {"status": "good job"}
        #return redirect(url_for('index'))

@bp.route('/<int:id>', methods=('GET',))
def get_one_release(id):
    release = get_release(id)
    return band

#at some point we'll need a get all bands by a user function 
#but get band by id is fine for now
def get_release(id):
    release = get_db().execute(
        'SELECT * FROM band WHERE id = ?',
        (id,)
    ).fetchone()

    if release is None:
        abort(404, f"Band id {id} doesn't exist.")
    
    return release

@bp.route('/<int:id>/update', methods=('POST',))
def update(id):
    release = get_release(id)

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
            'UPDATE release SET name = ? WHERE id = ?',
            (name, id)
        )
        db.commit()
        return {"status": "good job"}
        #return redirect(url_for('index'))


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_release(id)
    db = get_db()
    db.execute('DELETE FROM release WHERE id = ?', (id,))
    db.commit()
    return {"status": "good job"}
    #return redirect(for_url('index'))