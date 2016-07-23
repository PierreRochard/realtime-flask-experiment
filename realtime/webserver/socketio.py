from __future__ import absolute_import

import flask_socketio

from realtime.webserver.webapp import app

socketio = flask_socketio.SocketIO(app)


@socketio.on('connect', namespace='/')
def on_connect():
    print 'SocketIO connect /'


@socketio.on('disconnect', namespace='/')
def on_disconnect():
    print 'SocketIO disconnect /'


@socketio.on('connect', namespace='/browser')
def on_connect_browser():
    print 'SocketIO connect /browser'


@socketio.on('disconnect', namespace='/browser')
def on_disconnect_browser():
    print 'SocketIO disconnect /browser'


@socketio.on('connect', namespace='/worker')
def on_connect_worker():
    print 'SocketIO connect /worker'


@socketio.on('disconnect', namespace='/worker')
def on_disconnect_worker():
    print 'SocketIO disconnect /worker'
