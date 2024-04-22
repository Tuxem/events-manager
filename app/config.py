import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/concertdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
