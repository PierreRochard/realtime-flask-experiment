import json

import eventlet
import pgpubsub

from realtime.webserver.webapp import app
from realtime.webserver.socketio import socketio

eventlet.monkey_patch()
spawn = eventlet.spawn


def listen_thread():
    pubsub = pgpubsub.connect(user='Rochard', database='realtime')
    pubsub.listen('table_update')
    while True:
        for e in pubsub.events(yield_timeouts=True):
            if e is None:
                pass
            else:
                with app.app_context():
                    process_message(e)


def process_message(e):
    data = json.loads(e.payload)
    with open('output.json', 'w') as output:
        json.dump(data, output, indent=4, sort_keys=True)
    if data['type'] == 'INSERT':
        socketio.emit('insert', data['row'], namespace='/browser')
    elif data['type'] == 'UPDATE':
        socketio.emit('update', data['row'], namespace='/browser')
    elif data['type'] == 'DELETE':
        socketio.emit('delete', data['row'], namespace='/browser')


@app.before_first_request
def start_listener():
    spawn(listen_thread)
