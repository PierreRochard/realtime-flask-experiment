#!/usr/bin/env bash

createdb realtime;

psql -d realtime -c "CREATE SCHEMA flask";

pip2 install -r requirements.txt;

python2 manage.py db init;

python2 manage.py db migrate;

python2 manage.py db upgrade;

psql -d realtime -f realtime/database/create_triggers.sql