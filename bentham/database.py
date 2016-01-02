from peewee import Model, DateTimeField, IntegerField, CharField
from peewee import TextField, BooleanField, BlobField
from playhouse.postgres_ext import JSONField
from bentham import configObject


class Event(Model):
    class Meta:
        database = configObject.get_pg_db()
        db_table = 'events'

        indexes = (
            (('occurred_at', 'tracker', 'source_identifier',
              'event_hash', 'raw_event', 'raw_event_json'), True),
        )

    id = IntegerField()
    created_at = DateTimeField()
    occurred_at = DateTimeField()
    tracker = CharField()
    source_identifier = CharField()
    event_hash = BlobField()
    message = CharField()
    raw_event = TextField()
    raw_event_json = JSONField()
    ack = BooleanField()
