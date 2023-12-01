import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

con_str = f"""
dbname={os.getenv('POSTGRES_DB')}
user={os.getenv('POSTGRES_USER')}
password={os.getenv('POSTGRES_PASSWORD')}
host={os.getenv('POSTGRES_HOST')}
port={os.getenv('POSTGRES_PORT')}
"""

def get_conn():
    try:
        return psycopg2.connect(con_str)
    except Exception as error:
        print('connecting to database unsucessful')
        print('Error: ', error)

