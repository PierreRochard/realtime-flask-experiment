from __future__ import absolute_import

import flask

from . import views
from realtime.database.adapter import db


app = flask.Flask(__name__)
app.config.from_object('realtime.config')

app.register_blueprint(views.blueprint)
db.init_app(app)
