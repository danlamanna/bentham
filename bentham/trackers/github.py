from __future__ import absolute_import
from bentham.trackers import app, BenthamTrackerTask
from bentham.database import Event
from bentham.config import ConfigurationException, TrackerConfigException
import dateutil.parser
import json
import requests
import peewee

API_ROOT = "https://api.github.com/"


class GithubTrackerTask(BenthamTrackerTask):
    abstract = True

    @staticmethod
    def validate_tracker_config(tracker_config):
        BenthamTrackerTask.validate_tracker_config(tracker_config)
        if 'authentication' not in tracker_config:
            raise TrackerConfigException('"authentication" must be defined for {} tracker!'
                                         .format(tracker_config['name']))

    def get_auth(self, tracker_config):
        try:
            auth_key = tracker_config['authentication']
            return (self.config['authentication'][auth_key]['username'],
                    self.config['authentication'][auth_key]['access_token'])
        except KeyError:
            if 'authentication' not in tracker_config.keys():
                raise TrackerConfigException('Github trackers require an "authentication"'
                                             'attribute')
            else:
                auth_key = tracker_config['authentication']
                if auth_key not in self.config['authentication'].keys():
                    raise ConfigurationException('Authentication section "{}" not found'
                                                 .format(auth_key))

                if 'username' not in self.config['authentication'][auth_key].keys():
                    raise ConfigurationException('Github authentication methods require'
                                                 'a "username" attribute')
                if 'access_token' not in self.config['authentication'][auth_key].keys():
                    raise ConfigurationException('Github authentication methods require'
                                                 'an "access_token" attribute')


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

    def get_message_type(self, notification):
        return notification['reason']


@app.task(base=GithubTrackerTask, bind=True)
def notifications(self, tracker_config):
    GithubTrackerTask.validate_tracker_config(tracker_config)

    r = requests.get(API_ROOT + "notifications",
                     auth=self.get_auth(tracker_config))

    message_manager = NotificationMessageManager(tracker_config)

    for notification in r.json():
        try:
            Event(tracker=self.name,
                  occurred_at=dateutil.parser.parse(notification['updated_at']),
                  source_identifier=tracker_config['name'],
                  event_hash=notification['id'],
                  message=message_manager.parse(notification),
                  raw_event_json=json.dumps(notification)).save()
        except peewee.IntegrityError:
            # Some kind of error logging here?
            self.db.rollback()
