from flask import (
    Blueprint, flash, g, redirect, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.user import login_required
from flaskr.db import get_db

bp = Blueprint('review', __name__, url_prefix='/review')

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
            'INSERT INTO band (name) VALUES (?)',
            (name)
        )
        db.commit()
        return redirect(url_for('index'))

@bp.route('/<int:id>', methods=('GET',))
def get_one_review(id):
    review = get_review(id)
    return review

def get_review(id):
    review = get_db().execute(
        'SELECT * FROM review WHERE id = ?',
        (id,)
    ).fetchone()

    if review is None:
        abort(404, f"Review id {id} doesn't exist.")
    
    return review

@bp.route('/<int:id>/update', methods=('POST',))
def update(id):
    review = get_review(id)

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
            'UPDATE review SET name = ? WHERE id = ?',
            (name, id)
        )
        db.commit()
        return redirect(url_for('index'))


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_review(id)
    db = get_db()
    db.execute('DELETE FROM review WHERE id = ?', (id,))
    db.commit()
    return redirect(for_url('index'))