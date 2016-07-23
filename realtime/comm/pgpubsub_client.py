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
                    data = json.loads(e.payload)
                    with open('output.json', 'w') as output:
                        json.dump(data, output, indent=4, sort_keys=True)
                    if data['type'] == 'INSERT' or data['type'] == 'UPDATE':
                        data = data['row']
                        socketio.emit(
                            'new_update',
                            data['message'] + ' at ' + str(data['timestamp']),
                            namespace='/browser',
                        )


@app.before_first_request
def start_listener():
    print 'spawning pgpubsub'
    spawn(listen_thread)
