import os

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://localhost/realtime'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = os.urandom(24)
