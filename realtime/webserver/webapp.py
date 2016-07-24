from flask import Flask

from realtime.webserver import views
from realtime.database.adapter import db


app = Flask(__name__)
app.config.from_object('realtime.config')

app.register_blueprint(views.blueprint)
db.init_app(app)
