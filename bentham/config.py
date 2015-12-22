import os
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase

def config_file():
    if os.environ.has_key('BENTHAM_CONFIG'):
        return os.environ.get('BENTHAM_CONFIG')
    elif os.path.exists(os.path.expanduser('~/.config/bentham/config.yml')):
        return os.path.expanduser('~/.config/bentham/config.yml')
    elif os.path.exists('/etc/bentham.yml'):
        return '/etc/bentham.yml'
    else:
        raise Exception('No configuration file found.')

def get_config():
    with open(config_file(), 'rb') as infile:
        return yaml.load(infile)

def get_pg_db():
    config = get_config()

    return PostgresqlExtDatabase(config['datastore']['database'],
                                 **{k: v for k, v in config['datastore'].items() if \
                                    k not in ('type', 'database')})
