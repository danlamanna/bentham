from peewee import Model, DateTimeField, IntegerField, CharField, TextField, BooleanField
from playhouse.postgres_ext import JSONField
from bentham.config import Configuration

config = Configuration()

class Event(Model):
    class Meta:
        database = config.get_pg_db()
        db_table = 'events'

        indexes = (
            (('occurred_at', 'tracker', 'source_identifier', 'raw_event',
              'raw_event_json'), True),
        )

    id = IntegerField()
    created_at = DateTimeField()
    occurred_at = DateTimeField()
    tracker = CharField()
    source_identifier = CharField()
    message = CharField()
    raw_event = TextField()
    raw_event_json = JSONField()
    ack = BooleanField()
