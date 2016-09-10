import os
import uuid

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://localhost/realtime'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True

if not os.path.exists('secret_key'):
    with open('secret_key', 'w') as secret_key_file:
        SECRET_KEY = str(uuid.uuid4())
        secret_key_file.write(SECRET_KEY)
else:
    with open('secret_key', 'r') as secret_key_file:
        SECRET_KEY = secret_key_file.read()

SQLALCHEMY_BINDS = {'sessions_db': 'sqlite:///./sessions.db'}
