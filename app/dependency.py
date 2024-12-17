import psycopg2
import os

def get_database_connection():
    return psycopg2.connect(os.environ.get('DATABASE_CONNECTION'))
