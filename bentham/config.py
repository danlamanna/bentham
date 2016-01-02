import os
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase


class Configuration(object):
    def __init__(self):
        # Maintain a lazyloaded database conection so we
        # have a consistent reference to the connection so
        # we can do things like db.rollback() on the right
        # connection.
        self._db = None

    def load(self):
        with open(self.config_file(), 'rb') as infile:
            return yaml.load(infile) or {}

    def config_file(self):
        if os.path.exists(os.environ.get('BENTHAM_CONFIG', '')):
            return os.environ.get('BENTHAM_CONFIG')
        elif os.path.exists(os.path.expanduser('~/.config/bentham/config.yml')):
            return os.path.expanduser('~/.config/bentham/config.yml')
        elif os.path.exists('/etc/bentham.yml'):
            return '/etc/bentham.yml'
        else:
            raise Exception('No configuration file found.')

    def get_pg_db(self):
        config = self.load()

        try:
            if self._db is None:
                self._db = PostgresqlExtDatabase(
                    config['datastore']['database'],
                    **{k: v for k, v in config['datastore'].items() if
                       k not in ('type', 'database')})
            return self._db
        except KeyError:
            raise Exception('No datastore found in configuration.')
