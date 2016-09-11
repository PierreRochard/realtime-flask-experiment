import json

from flask import Flask

from realtime.database.adapter import db
from realtime.webserver import views


app = Flask(__name__)
app.config.from_object('realtime.config')

db.init_app(app)

views.admin.init_app(app)


@app.context_processor
def utility_processor():
    def get_row_ids(data, get_pk_value):
        table_name = str(data[0].__table__)
        row_ids = [get_pk_value(m) for m in data]
        row_ids = json.dumps({table_name: row_ids})
        return row_ids
    return dict(get_row_ids=get_row_ids)