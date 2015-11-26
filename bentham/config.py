import json
import pkg_resources as pr
from playhouse.postgres_ext import PostgresqlExtDatabase

def get_pg_db():
    conf_file = pr.resource_filename('bentham', 'conf/bentham.json')
    with open(conf_file, 'rb') as infile:
        credentials = json.load(infile)['database']

    db = PostgresqlExtDatabase(credentials['name'],
                               **{k: v for k, v in credentials.items() if k != 'name'})

    return db
