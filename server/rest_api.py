from flask import Flask, render_template
from flask_restful import Resource, Api

from server.models import db

app = Flask(__name__)
app.config.from_object('server.config')
db.init_app(app)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class UpdatesList(Resource):
    def get(self):
        updates = [u for u, in db.session.execute('SELECT row_to_json(t) AS j FROM flask.updates AS t;')]
        return updates

api.add_resource(UpdatesList, '/updates')
