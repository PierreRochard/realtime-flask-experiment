from flask import render_template, redirect, Blueprint, url_for

from realtime.database.models import Updates
from realtime.database.adapter import db

blueprint = Blueprint(__name__, __name__)


@blueprint.route('/')
def index():
    updates = Updates.query.all()
    return render_template('index.html', updates=updates)


@blueprint.route('/delete')
def delete():
    Updates.query.delete()
    db.session.commit()
    return redirect(url_for('.index'))
