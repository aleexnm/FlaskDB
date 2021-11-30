from os import environ, path
from dotenv import load_dotenv, find_dotenv
import sys

basedir = path.abspath(path.dirname(__file__))
load_dotenv(find_dotenv())


class AppConfig(object):
    SECRET_KEY = 'zvX47sfujgMktlhy-02B9A'
    db_user = environ.get('DATABASE_USERNAME')
    db_password = environ.get('DATABASE_PASSWORD')
    db_host = environ.get('DATABASE_HOST')
    # db_port = environ.get('DATABASE_PORT')
    db_name = environ.get('DATABASE_NAME')