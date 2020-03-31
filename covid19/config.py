from os import getenv
from dotenv import load_dotenv, find_dotenv
from playhouse.postgres_ext import PostgresqlExtDatabase
load_dotenv(find_dotenv())

# enviromanet variables
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
SENDGRID_API_KEY = getenv("SENDGRID_API_KEY")
TESTING = getenv('TESTING')
DATABASE_URL = getenv('DATABASE_URL')
PLATFORM = getenv('PLATFORM')


if PLATFORM != 'heroku':
    host = 'localhost'
    db = PostgresqlExtDatabase(POSTGRES_DB, user=POSTGRES_USER,
                               password=POSTGRES_PASSWORD, host=host, port=5432)
else:
    from playhouse.db_url import connect
    db = connect(DATABASE_URL)
