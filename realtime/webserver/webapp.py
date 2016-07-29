from flask import Flask

from realtime.webserver import views
from realtime.database.adapter import db


app = Flask(__name__)
app.config.from_object('realtime.config')

db.init_app(app)

views.admin.init_app(app)
