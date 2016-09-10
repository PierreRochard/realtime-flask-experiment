import json
import uuid

from flask import session

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from realtime.database.models import Updates, FlaskSessions
from realtime.database.adapter import db

admin = Admin(name='realtime', template_mode='bootstrap3', url='/')


class RealtimeModelView(ModelView):
    list_template = 'realtime.html'
    column_default_sort = ('id', True)
    column_display_pk = True

    def pre_render_function(self, data):
        if not session.get('session_id'):
            session['session_id'] = str(uuid.uuid4())
            new_flask_session = dict(session)
            new_flask_session = FlaskSessions(**new_flask_session)
            db.session.add(new_flask_session)
            db.session.commit()
        else:
            existing_flask_session = (
                db.session.query(FlaskSessions)
                    .filter(FlaskSessions.session_id == session['session_id'])
                    .first()
            )
            if not existing_flask_session:
                new_flask_session = dict(session)
                new_flask_session = FlaskSessions(**new_flask_session)
                db.session.add(new_flask_session)
                db.session.commit()
        table_name = str(self.model.__table__)
        ids = [self.get_pk_value(m) for m in data]
        ids = json.dumps({table_name: ids})
        self._template_args['ids'] = ids
        self._template_args['session_id'] = session['session_id']


admin.add_view(RealtimeModelView(Updates, db.session))
