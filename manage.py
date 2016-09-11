import random
import string
from datetime import datetime

import flask_migrate
import flask_script
import time
from sqlalchemy import func

from realtime.database import models
from realtime.database.adapter import db
from realtime.database.models import Updates
import realtime.database.pgpubsub_client
from realtime.webserver.socket_io import socket_io
from realtime.webserver.webapp import app

manager = flask_script.Manager(app)
flask_migrate.Migrate(app, db)
manager.add_command('db', flask_migrate.MigrateCommand)


@manager.command
def runserver(debug=True, use_reloader=True):
    db.drop_all(bind='sessions_db')
    db.create_all(bind='sessions_db')
    socket_io.run(app, port=5001, debug=debug, use_reloader=use_reloader)


@manager.command
def add():
    for i in range(0, 40):
        u = Updates(message='Added from command-line')
        with app.app_context():
            print('Committing to database ...')
            db.session.add(u)
            db.session.commit()
        print('Added.')


@manager.command
def update():
    with app.app_context():
        while True:
            update = (
                db.session.query(Updates)
                            .order_by(func.random())
                            .first()
            )
            update.message = ''.join(random.choice(string.ascii_lowercase)
                                     for x in range(20))
            update.timestamp = datetime.now()
            db.session.commit()
            time.sleep(0.1)


@manager.command
def delete():
    with app.app_context():
        models.Updates.query.delete()
        db.session.commit()
    print('Deleted all updates.')


@manager.command
def create_dbs():
    with app.app_context():
        db.create_all()
        db.create_all(bind='sessions_db')


if __name__ == '__main__':
    manager.run()
