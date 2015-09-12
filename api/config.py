import json
from playhouse.postgres_ext import PostgresqlExtDatabase

def get_pg_db():
    with open('../bentham.json', 'rb') as infile:
        credentials = json.load(infile)['database']

    db = PostgresqlExtDatabase(credentials['name'],
                               **{k: v for k, v in credentials.items() if k != 'name'})

    return db
