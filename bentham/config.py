import os
import yaml


class Configuration(object):
    def __init__(self):
        # Maintain a lazyloaded database conection so we
        # have a consistent reference to the connection so
        # we can do things like db.rollback() on the right
        # connection.
        self._db = None

    def load(self, *parts):
        if parts:
            filename = os.path.join(self.config_path(), *parts)
        else:
            filename = os.path.join(self.config_path(), 'config.yml')

        with open(filename, 'rb') as infile:
            return yaml.load(infile) or {}

    def config_path(self):
        if os.path.exists(os.environ.get('BENTHAM_CONFIG', '')):
            return os.environ.get('BENTHAM_CONFIG')
        elif os.path.exists(os.path.expanduser('~/.config/bentham')):
            return os.path.expanduser('~/.config/bentham')
        elif os.path.exists('/etc/bentham'):
            return '/etc/bentham'
        else:
            raise Exception('No configuration dir found.')

    def get_pg_db(self):
        config = self.load()

        try:
            if self._db is None:
                from bentham.database import metadata
                from sqlalchemy import create_engine

                engine = create_engine(config['datastore']['uri'])
                metadata.create_all(engine)
                self._db = engine.connect()
            return self._db
        except KeyError:
            raise Exception('No datastore found in configuration.')
