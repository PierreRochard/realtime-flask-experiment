from __future__ import absolute_import

import datetime

from .adapter import db


class Updates(db.Model):
    __table_args__ = ({'schema': 'flask'}, )
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.String(128))

    def __repr__(self):
        return r'<Updates "%s" at %s>' % (self.message, self.timestamp)
