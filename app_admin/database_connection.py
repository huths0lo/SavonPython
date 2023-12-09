import sqlalchemy
import pandas.io.sql as psql
from app_admin.check_create_db import find_db_else_create_new

db_file = find_db_else_create_new()
db_uri = f'sqlite:///{db_file}'




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


