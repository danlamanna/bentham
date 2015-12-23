from __future__ import absolute_import
from bentham.trackers import app
from bentham import configObject
from bentham.database import Event

from celery import Task


def recursive_fib(n):
    if n < 2:
        return n
    return recursive_fib(n - 2) + recursive_fib(n - 1)


class BenthamTrackerTask(Task):
    abstract = True
    _db = None
    _event = None

    @property
    def db(self):
        if self._db is None:
            self._db = configObject.get_pg_db()

        return self._db

    @property
    def event(self):
        if self._event is None:
            self._event = Event

        return self._event


@app.task
def async_fib(n):
    return recursive_fib(n)


@app.task(base=BenthamTrackerTask)
def track_something():
    from datetime import datetime

    track_something.event(occurred_at=datetime.now(),
                          tracker='some-tracker',
                          source_identifier='some-source',
                          message='some-message',
                          raw_event='some-event').save()
