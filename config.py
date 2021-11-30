from os import environ, path
from dotenv import dotenv_values

config = dotenv_values()

class AppConfig(object):
    SECRET_KEY = 'zvX47sfujgMktlhy-02B9A'
    db_user = config['DATABASE_USERNAME']
    db_password = config['DATABASE_PASSWORD']
    db_host = config['DATABASE_HOST']
    # db_port = environ.get('DATABASE_PORT')
    db_name = config['DATABASE_NAME']