# realtime-flask-experiment
Experimenting with PostgreSQL's Listen/Notify and Flask-SocketIO

Blog post: https://rochard.org/personal-projects/realtime-flask-with-socketio-and-postgresql/

Flask part is largely from https://github.com/lukeyeager/flask-sqlalchemy-socketio-demo

PostgreSQL part is largely from https://blog.andyet.com/2015/04/06/postgres-pubsub-with-json/


### Setup
The install.sh assumes that you are on your local dev pg instance that doens't have a password. If that's not the case you'll have to open up a terminal and modify the commands as needed.
```
bash install.sh
python manage.py runserver
Open your browser and navigate to localhost:5001
python manage.py add
```
