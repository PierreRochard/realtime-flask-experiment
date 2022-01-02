#!/usr/bin/env bash

createdb realtime;

psql -d realtime -c "CREATE SCHEMA flask";

pip install -r requirements.txt;

flask db init;

flask db migrate;

flask db upgrade;

psql -d realtime -f realtime/database/create_functions.sql

psql -d realtime -f realtime/database/create_triggers.sql