from flask import session, request

from flask_socketio import SocketIO

from realtime.webserver.webapp import app
from realtime.database.adapter import db
from realtime.database.models import SocketIoSessions, SessionRows

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
def on_message(message):
    for table_name in message:
        for row_id in message[table_name]:
            new_row = SessionRows(row_id=row_id, table_name=table_name,
                                  socket_io_id=request.sid)
            db.session.add(new_row)
            db.session.commit()


@socketio.on('disconnect', namespace='/browser')
def on_disconnect_browser():
    (
        db.session.query(SocketIoSessions)
            .filter(SocketIoSessions.socket_io_id == request.sid)
            .delete()
    )
    (
        db.session.query(SessionRows)
            .filter(SessionRows.socket_io_id == request.sid)
            .delete()
    )
    db.session.commit()

    print('SocketIO disconnect /browser')
