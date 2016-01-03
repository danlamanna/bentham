from __future__ import absolute_import
from celery import Celery, Task
from bentham import configObject
from bentham.database import Event
from datetime import timedelta
from bentham.config import TrackerConfigException


class BenthamTrackerTask(Task):
    abstract = True
    _db = None
    _event = None
    _config = None

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

    @property
    def config(self):
        if self._config is None:
            self._config = configObject.load()
        return self._config

    @staticmethod
    def validate_tracker_config(tracker_config):
        if 'name' not in tracker_config.keys():
            raise TrackerConfigException('"name" must be defined in tracker!')
        if 'task' not in tracker_config.keys():
            raise TrackerConfigException('"tracker" must be defined for {} tracker!'
                                         .format(tracker_config['name']))
        if 'interval' not in tracker_config.keys():
            raise TrackerConfigException('"interval" must be defined for {} tracker!'
                                         .format(tracker_config['name']))


class Schedule(object):
    def __init__(self, config):
        self.config = config.load()

    def get_schedule(self):
        schedule = {}

        # Should assert all tracker names are unique
        for tracker in self.config['trackers']:
            # Should validate 'tracker' section of config
            schedule[tracker['name']] = {
                'task': tracker['task'],
                'schedule': timedelta(seconds=tracker['interval']),
                'args': (tracker, )
            }

        return schedule

app = Celery('bentham',
             broker='amqp://rabbit:rabbit@localhost',
             backend='amqp://rabbit:rabbit@localhost',
             include=['bentham.trackers.fib',
                      'bentham.trackers.github'])

# Optional configuration, see the application user guide.

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_SEND_EVENTS=True,
    CELERY_SEND_TASK_SENT_EVENT=True,
    CELERYBEAT_SCHEDULE=Schedule(configObject).get_schedule()
)

if __name__ == '__main__':
    app.start()
