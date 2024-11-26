import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_zarif')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///marketplace.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
