import flask_migrate
import flask_script

from realtime.database import models
from realtime.database.adapter import db
from realtime.database.models import Updates
from realtime.webserver.socketio import socketio
from realtime.webserver.webapp import app
import realtime.comm.pgpubsub_client

manager = flask_script.Manager(app)
flask_migrate.Migrate(app, db)
manager.add_command('db', flask_migrate.MigrateCommand)


@manager.command
def runserver(debug=True, use_reloader=False):
    socketio.run(app, port=5001, debug=debug, use_reloader=use_reloader)


@manager.command
def add():
    for i in range(0, 10):
        u = Updates(message='Added from command-line')
        with app.app_context():
            print('Committing to database ...')
            db.session.add(u)
            db.session.commit()
        print('Added.')


@manager.command
def delete():
    with app.app_context():
        models.Updates.query.delete()
        db.session.commit()
    print('Deleted all updates.')


if __name__ == '__main__':
    manager.run()
