import os

from flask import Flask, render_template, session, request
from flask_restful import Resource, Api
from flask_session import Session
from flask_redis import FlaskRedis
from server.models import db

app = Flask(__name__)
app.config.from_object('server.config')
app.secret_key = os.urandom(24)
db.init_app(app)
api = Api(app)
Session(app)
redis_store = FlaskRedis(app)


@app.route('/')
def index():
    return render_template('index.html')


class UpdatesList(Resource):
    def get(self):
        updates = list(db.session.execute('SELECT t.id, row_to_json(t) AS j FROM flask.updates AS t LIMIT 5;'))
        # [redis_store.lpush('updates-' + str(i), redis_store.get(request.cookies['session'])) for i, j in updates]
        updates = [j for i, j in updates]
        return updates

api.add_resource(UpdatesList, '/updates')
