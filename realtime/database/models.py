import datetime

from realtime.database.adapter import db


class Updates(db.Model):
    __table_args__ = ({'schema': 'flask'},
                      )
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.String(128))

    def __repr__(self):
        return r'<Updates "%s" at %s>' % (self.message, self.timestamp)


class SessionRows(db.Model):
    __bind_key__ = 'sessions_db'
    __tablename__ = 'session_rows'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    row_id = db.Column(db.Integer)
    table_name = db.Column(db.String)

    socket_io_id = db.Column(db.String)
