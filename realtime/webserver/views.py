from flask import render_template, redirect, Blueprint, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from realtime.database.models import Updates
from realtime.database.adapter import db

admin = Admin(name='realtime', template_mode='bootstrap3', url='/')

class RealtimeModelView(ModelView):
    list_template = 'realtime.html'

admin.add_view(RealtimeModelView(Updates, db.session))

# @blueprint.route('/')
# def index():
#     updates = Updates.query.all()
#     return render_template('index.html', updates=updates)
#
#
# @blueprint.route('/delete')
# def delete():
#     Updates.query.delete()
#     db.session.commit()
#     return redirect(url_for('.index'))
