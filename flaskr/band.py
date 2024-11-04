from flask import (
    Blueprint, flash, g, redirect, request, url_for, jsonify
)
import json
from werkzeug.exceptions import abort

from flaskr.user import login_required
from flaskr.db import get_db

bp = Blueprint('band', __name__, url_prefix='/band')

#TODO - this needs to be paginated
@bp.route('/')
def get_all_bands():
    db = get_db()
    bands = db.execute(
        'SELECT * FROM band'
    ).fetchall()
    return json.dumps( [dict(band) for band in bands] )

@bp.route('/create', methods=('POST',))
def create():
    name = request.form['name']
    status = request.form['status']
    band_picture = request.form['band_picture']
    error = None

    if not name:
        error = 'Name is required.'
    if not status:
        error = 'Status is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO band (name, status, band_picture) VALUES (?,?,?)',
            (name, status, band_picture)
        )
        db.commit()
        return {"status": "good job"}
        #return redirect(url_for('index'))

@bp.route('/<int:id>', methods=('GET',))
def get_one_band(id):
    band = get_band_with_metadata(id)
    band_formatted = build_formatted_response(band)
    return json.dumps( band_formatted )

def build_formatted_response(band):
    band_formatted = {}

    band_info_dict = dict(band[0])
    band_formatted['name'] = band_info_dict['name']
    band_formatted['status'] = band_info_dict['status']
    band_formatted['band_picture'] = band_info_dict['band_picture']

    band_formatted['releases'] = []

    for b in band:
        current_dict = dict(b)
        release = {
            'release_id': current_dict['release_id'],
            'year': current_dict['year'],
            'name': current_dict['name'],
            'review_avg': current_dict['review_avg'],
            'review_count': current_dict['review_count']
        }
        band_formatted['releases'].append(release)
    
    return band_formatted


# pulling band + release list and avg / count for reviews by release
def get_band_with_metadata(id):
    band_with_metadata = get_db().execute(
        'SELECT a.name, a.status, a.band_picture, b.id as release_id, b.year, b.name, AVG(c.score) as review_avg, COUNT(c.id) as review_count FROM band a LEFT JOIN releases b on b.band_id = a.id LEFT JOIN reviews c on c.release_id = b.id WHERE a.id = ? GROUP BY b.id',
        (id,)
    ).fetchall()

    if band_with_metadata is None:
        abort(404, f"Band id {id} doesn't exist.")

    return band_with_metadata


def get_band(id):
    band = get_db().execute(
        'SELECT * FROM band WHERE id = ?',
        (id,)
    ).fetchone()

    if band is None:
        abort(404, f"Band id {id} doesn't exist.")
    
    print(band)

    return band

@bp.route('/<int:id>/update', methods=('POST',))
def update(id):
    band = get_band(id)

    #build out as band object expands
    #has to be a better way to do this to be more dynamic
    name = request.form['name']
    status = request.form['status']
    band_picture = request.form['band_picture']
    error = None

    if not name:
        error = 'Name is required.'
    if not status:
        error = 'Status is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'UPDATE band SET name = ?, status = ?, band_picture = ? WHERE id = ?',
            (name, status, band_picture, id)
        )
        db.commit()
        return {"status": "good job"}
        #return redirect(url_for('index'))


#TODO - delete a band should delete all meta associated to band
#EG. releases / reviews / etc
@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_band(id)
    db = get_db()
    db.execute('DELETE FROM band WHERE id = ?', (id,))
    db.commit()
    return {"status": "good job"}
    #return redirect(for_url('index'))
