from flask import session, request

from flask_socketio import SocketIO

from realtime.webserver.webapp import app
from realtime.database.adapter import db
from realtime.database.models import SocketIoSessions

socketio = SocketIO(app)


@socketio.on('connect', namespace='/')
def on_connect():
    print('SocketIO connect /')


@socketio.on('disconnect', namespace='/')
def on_disconnect():
    print('SocketIO disconnect /')


@socketio.on('connect', namespace='/browser')
def on_connect_browser():
    session['socket_io_id'] = request.sid
    new_socket_io_session = dict(session)
    new_socket_io_session = SocketIoSessions(**new_socket_io_session)
    db.session.add(new_socket_io_session)
    db.session.commit()
    print('SocketIO connect /browser')


@socketio.on('ids', namespace='/browser')
def on_ids(message):
    print(message)


@socketio.on('disconnect', namespace='/browser')
def on_disconnect_browser():
    disconnected_session = (
        db.session.query(SocketIoSessions)
            .filter(SocketIoSessions.socket_io_id == session['socket_io_id'])
            .one()
    )
    db.session.delete(disconnected_session)
    db.session.commit()
    print('SocketIO disconnect /browser')
