import os
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase

class Configuration(object):

    config = None

    def __init__(self):
        return self.load()

    def load(self):
        if not self.config:
            with open(self.config_file(), 'rb') as infile:
                self.config = yaml.load(infile)

        return self.config

    def config_file(self):
        if os.environ.has_key('BENTHAM_CONFIG'):
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
            return PostgresqlExtDatabase(config['datastore']['database'],
                                         **{k: v for k, v in config['datastore'].items() if \
                                            k not in ('type', 'database')})
        except KeyError:
            raise Exception('No datastore found in configuration.')
