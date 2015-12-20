from peewee import Model, DateTimeField, IntegerField, CharField, TextField, BooleanField, PostgresqlDatabase
from playhouse.postgres_ext import JSONField

from config import get_pg_db

database = PostgresqlDatabase('bentham', **{'host': '192.168.13.37', 'password': 'bentham', 'user': 'bentham'})

class Event(Model):
    class Meta:
        database = database
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
