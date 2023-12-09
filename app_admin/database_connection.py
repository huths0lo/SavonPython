import sqlalchemy
import pandas.io.sql as psql
import os
from dotenv import load_dotenv
import sys

load_dotenv()



db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_server = os.getenv('db_server')
db_port = os.getenv('db_port')
db_uri = f'postgresql://{db_user}:{db_pass}@{db_server}:{db_port}/savonpy_db'




def execute_db(query):
    engine = sqlalchemy.create_engine(db_uri, pool_size=10, max_overflow=20)
    with engine.connect() as conn, conn.begin():
        conn.execute(sqlalchemy.text(query))
    engine.dispose()

def query_db(query):
    engine = sqlalchemy.create_engine(db_uri)
    response = psql.read_sql_query(query, con=engine)
    engine.dispose()
    return response


def test_db_con():
    try:
        query_db("SELECT now()")
    except:
        print('Unable to connect to database.  Exiting!/n')
        sys.exit()


test_db_con()