import uuid

from flask import request, session

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from realtime.database.models import Updates
from realtime.database.adapter import db

admin = Admin(name='realtime', template_mode='bootstrap3', url='/')


class RealtimeModelView(ModelView):
    list_template = 'realtime.html'

    def pre_render_function(self):
        session['session_id'] = uuid.uuid4()
        print(request)
        from pprint import pformat
        print(pformat(dir(request)))
        print(session)
        from pprint import pformat
        print(pformat(dir(session)))
        print(session.keys())


admin.add_view(RealtimeModelView(Updates, db.session))
