import os
from os.path import dirname, join, abspath
from dotenv import load_dotenv


BASE_DIR = abspath(join(dirname(__file__), ".."))
DOTENV_PATH = join(BASE_DIR, "instance", ".env")
load_dotenv(DOTENV_PATH)


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
    # Railway/Production
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
