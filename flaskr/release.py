from flask import (
    Blueprint, flash, g, redirect, request, url_for, jsonify
)
import json
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
    return json.dumps([dict(release)])

#at some point we'll need a get all bands by a user function
#but get band by id is fine for now
def get_release(id):
    release = get_db().execute(
        'SELECT a.name, a.year, a.art, a.release_type, a.band_id, b.name as band_name FROM releases a INNER JOIN band b on b.id = a.band_id WHERE a.id = ?',
        (id,)
    ).fetchone()

    if release is None:
        abort(404, f"Release id {id} doesn't exist.")

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
            'UPDATE releases SET name = ? WHERE id = ?',
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