from datetime import datetime
from peewee import Model, DateTimeField, IntegerField, CharField
from playhouse.postgres_ext import BinaryJSONField

from config import get_pg_db

db = get_pg_db()

class Event(Model):
    class Meta:
        database = db

        indexes = (
            (('occurred_at', 'message'), True),
        )

    created_at = DateTimeField(default=datetime.now)
    occurred_at = DateTimeField(default=datetime.now)
    priority = IntegerField()
    message = CharField()
    raw = CharField()
    raw_json = BinaryJSONField()
