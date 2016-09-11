from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from realtime.database.models import Updates
from realtime.database.adapter import db

admin = Admin(name='realtime', template_mode='bootstrap3', url='/')


class RealtimeModelView(ModelView):
    list_template = 'realtime.html'
    column_default_sort = ('id', True)
    column_display_pk = True


admin.add_view(RealtimeModelView(Updates, db.session))
