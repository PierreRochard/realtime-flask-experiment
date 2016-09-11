from flask import request

from flask_socketio import SocketIO

from realtime.database.adapter import db
from realtime.database.models import SessionRows
from realtime.webserver.webapp import app

socket_io = SocketIO(app)


@socket_io.on('connect', namespace='/')
def on_connect():
    pass


@socket_io.on('row_ids', namespace='/')
def on_message(message):
    for table_name in message:
        for row_id in message[table_name]:
            new_row = SessionRows(row_id=row_id, table_name=table_name,
                                  socket_io_id=request.sid)
            db.session.add(new_row)
            db.session.commit()


@socket_io.on('disconnect', namespace='/')
def on_disconnect():
    (
        db.session.query(SessionRows)
            .filter(SessionRows.socket_io_id == request.sid)
            .delete()
    )
    db.session.commit()
