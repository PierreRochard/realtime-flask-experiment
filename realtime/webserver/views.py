from __future__ import absolute_import

import flask

from realtime.database.models import Updates
from realtime.database.adapter import db

blueprint = flask.Blueprint(__name__, __name__)



@blueprint.route('/')
def index():
    updates = Updates.query.all()
    return flask.render_template('index.html', updates=updates)


@blueprint.route('/delete')
def delete():
    Updates.query.delete()
    db.session.commit()
    return flask.redirect(flask.url_for('.index'))
