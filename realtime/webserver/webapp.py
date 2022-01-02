from datetime import datetime
import json
import random
import string
import time

import eventlet
from flask import Flask, request
from flask_migrate import Migrate
from flask_socketio import SocketIO
from sqlalchemy import func
import pgpubsub

from realtime.database import models
from realtime.database.adapter import db
from realtime.database.models import TodoItems, Subscriptions
from realtime.webserver import views

app = Flask(__name__)
app.config.from_object('realtime.config')

db.init_app(app)
socket_io = SocketIO(app)
migrate = Migrate(app, db)

views.admin.init_app(app)


def listen_thread():
    pubsub = pgpubsub.connect(database='realtime')
    pubsub.listen('todo_items_table_update')
    while True:
        for event in pubsub.events(yield_timeouts=True):
            if event is None:
                pass
            else:
                with app.app_context():
                    process_message(event)


@app.before_first_request
def start_listener():
    eventlet.monkey_patch()
    spawn = eventlet.spawn
    spawn(listen_thread)


def process_message(event):
    data = json.loads(event.payload)
    with open('output.json', 'w') as output:
        json.dump(data, output, indent=4, sort_keys=True)
    # TODO: Query the table if 'row' is not in the data dictionary
    # (due to pg_notify's 8kB payload limit)
    if data['type'] == 'INSERT':
        socket_io.emit('insert', data['row'], namespace='/')
    elif data['type'] == 'UPDATE':
        socket_io_clients = (
            db.session.query(Subscriptions.socket_io_id)
                .filter(Subscriptions.record_id == data['id'])
                .filter(Subscriptions.table_name == data['table_name'])
                .group_by(Subscriptions.socket_io_id)
                .all()
        )
        for client, in socket_io_clients:
            socket_io.emit('update',
                           data['row'],
                           namespace='/',
                           room=client)
    elif data['type'] == 'DELETE':
        socket_io.emit('delete', data['row'], namespace='/')


@app.context_processor
def utility_processor():
    def get_record_ids(data, get_pk_value):
        table_name = str(data[0].__table__)
        record_ids = [get_pk_value(m) for m in data]
        record_ids = json.dumps({table_name: record_ids})
        return record_ids

    return dict(get_record_ids=get_record_ids)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, TodoItems=TodoItems)


@app.cli.command()
def runserver(debug=True, use_reloader=True):
    db.drop_all(bind='sessions_db')
    db.create_all(bind='sessions_db')
    socket_io.run(app, port=5001, debug=debug, use_reloader=use_reloader)


@app.cli.command()
def add():
    for i in range(0, 40):
        u = TodoItems(title='Todo Item')
        with app.app_context():
            db.session.add(u)
            db.session.commit()


@app.cli.command()
def update():
    with app.app_context():
        while True:
            update = (
                db.session.query(TodoItems)
                    .order_by(func.random())
                    .first()
            )
            update.title = ''.join(random.choice(string.ascii_lowercase)
                                   for x in range(20))
            update.timestamp = datetime.now()
            db.session.commit()
            time.sleep(0.1)


@app.cli.command()
def delete():
    with app.app_context():
        models.TodoItems.query.delete()
        db.session.commit()
    print('Deleted all updates.')


@app.cli.command()
def create_dbs():
    with app.app_context():
        db.create_all()
        db.create_all(bind='sessions_db')


@socket_io.on('connect', namespace='/')
def on_connect():
    pass


@socket_io.on('record_ids', namespace='/')
def on_message(message):
    for table_name in message:
        for record_id in message[table_name]:
            new_row = Subscriptions(record_id=record_id, table_name=table_name,
                                    socket_io_id=request.sid)
            db.session.add(new_row)
            db.session.commit()


@socket_io.on('disconnect', namespace='/')
def on_disconnect():
    (
        db.session.query(Subscriptions)
            .filter(Subscriptions.socket_io_id == request.sid)
            .delete()
    )
    db.session.commit()
