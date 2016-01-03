from __future__ import absolute_import
from bentham.trackers import app, BenthamTrackerTask
from bentham.database import Event
import dateutil.parser
import json
import requests
import peewee

API_ROOT = "https://api.github.com/"


class GithubMessageManager(object):
    default_message_format = "Generic Github Event"

    def __init__(self, config):
        self.config = config

    def get_message_format(self, event_type):
        try:
            return self.config['message_formats'][event_type]
        except KeyError:
            return self.default_message_format

    def get_default_data(self, notification):
        raise Exception("get_default_data must be implemented in a child class!")

    def get_message_type(self, event):
        raise Exception("get_message_type must be implemented in a child class!")

    def parse(self, event):
        message_type = self.get_message_type(event)
        signature = "get_{}_data".format(message_type)

        if hasattr(self, signature) and hasattr(getattr(self, signature), "__call__"):
            message_data = getattr(self, signature)(event)
        else:
            message_data = self.get_default_data(event)

        return self.get_message_format(message_type).format(**message_data)


class NotificationMessageManager(GithubMessageManager):
    default_message_format = "{type} on {repo}: {title}"

    def get_default_data(self, notification):
        return {
            'id': notification['id'],
            "reason": notification['reason'],
            'repo': notification['repository']['full_name'],
            'title': notification['subject']['title'],
            'type': notification['subject']['type'],
            'url': notification['subject']['url']
        }

    def get_message_type(self, event):
        return event['reason']


@app.task(base=BenthamTrackerTask, bind=True)
def notifications(self, config):

    auth = (config['username'], config['access_token'])
    r = requests.get(API_ROOT + "notifications", auth=auth)

    message_manager = NotificationMessageManager(config)

    for notification in r.json():
        try:
            Event(tracker=self.name,
                  occurred_at=dateutil.parser.parse(notification['updated_at']),
                  source_identifier=config['name'],
                  event_hash=notification['id'],
                  message=message_manager.parse(notification),
                  raw_event_json=json.dumps(notification)).save()
        except peewee.IntegrityError:
            self.db.rollback()
            # Some kind of error logging here?
