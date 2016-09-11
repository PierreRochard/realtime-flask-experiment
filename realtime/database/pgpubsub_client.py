import json

import eventlet
import pgpubsub

from realtime.database.adapter import db
from realtime.database.models import SessionRows
from realtime.webserver.socket_io import socket_io
from realtime.webserver.webapp import app

eventlet.monkey_patch()
spawn = eventlet.spawn


def listen_thread():
    pubsub = pgpubsub.connect(database='realtime')
    pubsub.listen('table_update')
    while True:
        for event in pubsub.events(yield_timeouts=True):
            if event is None:
                pass
            else:
                with app.app_context():
                    process_message(event)


def process_message(event):
    data = json.loads(event.payload)
    with open('output.json', 'w') as output:
        json.dump(data, output, indent=4, sort_keys=True)
    # TODO: Query the table if 'row' is not in the data dictionary
    # (due to pg_notify's 8kB payload limit)
    if data['type'] == 'INSERT':
        socket_io.emit('insert', data['row'], namespace='/')
    elif data['type'] == 'UPDATE':
        socket_io_clients = (
            db.session.query(SessionRows.socket_io_id)
                .filter(SessionRows.row_id == data['id'])
                .filter(SessionRows.table_name == data['table_name'])
                .group_by(SessionRows.socket_io_id)
                .all()
        )
        for client, in socket_io_clients:
            socket_io.emit('update',
                           data['row'],
                           namespace='/',
                           room=client)
    elif data['type'] == 'DELETE':
        socket_io.emit('delete', data['row'], namespace='/')


@app.before_first_request
def start_listener():
    spawn(listen_thread)
