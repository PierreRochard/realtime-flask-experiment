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
    def get_record_ids(data, get_pk_value):
        table_name = str(data[0].__table__)
        record_ids = [get_pk_value(m) for m in data]
        record_ids = json.dumps({table_name: record_ids})
        return record_ids
    return dict(get_record_ids=get_record_ids)
