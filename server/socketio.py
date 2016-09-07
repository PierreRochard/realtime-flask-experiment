from flask import session, request
from flask_socketio import SocketIO

from server.rest_api import app, redis_store

socketio = SocketIO(app)


@socketio.on('connect')
def on_connect_browser():
    print('SocketIO connect ', request.sid)
    redis_store.set(session.sid, request.sid)


@socketio.on('disconnect')
def on_disconnect_browser():
    print('SocketIO disconnect ', request.sid)
