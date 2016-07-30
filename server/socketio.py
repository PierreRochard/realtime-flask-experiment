from flask_socketio import SocketIO

from server.rest_api import app

socketio = SocketIO(app)


@socketio.on('connect', namespace='/')
def on_connect():
    print('SocketIO connect /')


@socketio.on('disconnect', namespace='/')
def on_disconnect():
    print('SocketIO disconnect /')


@socketio.on('connect', namespace='/browser')
def on_connect_browser():
    print('SocketIO connect /browser')


@socketio.on('disconnect', namespace='/browser')
def on_disconnect_browser():
    print('SocketIO disconnect /browser')
