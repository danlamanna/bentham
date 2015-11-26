import requests
import json
from time import sleep
import twitter

class EventTracker(object):
    def __init__(self, interval):
        self.interval = interval

    def track(self):
        pass

class TwitterEventTracker(EventTracker):
    identifier = 'twitter_dan_lamanna'

    def __init__(self, interval):
        super(TwitterEventTracker, self).__init__(interval)
        self.api = twitter.Api(consumer_key='',
                               consumer_secret='',
                               access_token_key='',
                               access_token_secret='')

        self.since_id = 0

    def event_repr(self, event):
        return '%s mentioned you: %s' % (event['user']['screen_name'],
                                         event['text'])

    def track(self):
        mentions = self.api.GetMentions(since_id=self.since_id)

        for mention in mentions:
            mention = mention.AsDict()
            requests.put('http://127.0.0.1:8080/api/logs',
                         json={'occurred_at': mention['created_at'],
                               'priority': 10,
                               'message': self.event_repr(mention),
                               'raw_json': mention})

    def run(self):
        while True:
            self.track()
            sleep(self.interval.get())
