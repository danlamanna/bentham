from __future__ import absolute_import
from bentham.trackers import app, BenthamTrackerTask


@app.task(base=BenthamTrackerTask, bind=True)
def events(self, config):
    from datetime import datetime

    with open("", "a") as fh:
        fh.write("%s\n", datetime.now().isoformat())

#    self.event(occurred_at=datetime.now(),
#               tracker='some-tracker',
#               source_identifier='some-source',
#               message='some-message',
#               raw_event='some-event').save()
