#!/usr/bin/env bash

createdb realtime;

psql -d realtime -c "CREATE SCHEMA flask";

pip install -r requirements.txt;

python manage.py db init;

python manage.py db migrate;

python manage.py db upgrade;

psql -d realtime -f realtime/database/create_triggers.sql