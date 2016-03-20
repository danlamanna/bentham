from github3 import login
from bentham.database import events
from sqlalchemy.exc import IntegrityError

TRACKER_ID = 'github'


def track(source, db, cfg):
    github = login(token=cfg['auth']['token'])

    for notification in github.iter_notifications():
        try:
            db.execute(events.insert(),
                       occurred_at=notification.updated_at,
                       tracker=TRACKER_ID,
                       source=source,
                       message=notification.subject['title'],
                       raw_json=notification.to_json())
        except IntegrityError:
            pass  # duplicate row
