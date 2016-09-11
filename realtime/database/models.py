import datetime

from realtime.database.adapter import db


class TodoItems(db.Model):
    __table_args__ = ({'schema': 'flask'},
                      )
    __tablename__ = 'todo_items'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(128))

    def __repr__(self):
        return r'<TodoItems "%s" at %s>' % (self.title, self.timestamp)


class Subscriptions(db.Model):
    __bind_key__ = 'sessions_db'
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    record_id = db.Column(db.Integer)
    table_name = db.Column(db.String)

    socket_io_id = db.Column(db.String)
