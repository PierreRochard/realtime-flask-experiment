from flask import render_template, redirect, Blueprint, url_for

from realtime.database.models import Updates
from realtime.database.adapter import db

blueprint = Blueprint(__name__, __name__)


@blueprint.route('/')
def index():
    updates = db.session.execute('SELECT row_to_json(t) as j from flask.updates as t;')
    updates_json = [u for u, in updates]
    columns = [k for k in updates_json[0]]
    return render_template('index.html', updates=updates_json, columns=columns)


@blueprint.route('/delete')
def delete():
    Updates.query.delete()
    db.session.commit()
    return redirect(url_for('.index'))
