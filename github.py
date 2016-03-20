from github3 import login
from bentham.database import events
from bentham.utils import bentham_tracker
from sqlalchemy.exc import IntegrityError


@bentham_tracker('github', 'danlamanna')
def github_tracker(tracker, source, db, cfg):
    github = login(token=cfg['auth']['token'])

    for notification in github.iter_notifications():
        try:
            db.execute(events.insert(),
                       occurred_at=notification.updated_at,
                       tracker=tracker,
                       source=source,
                       message=notification.subject['title'],
                       raw_json=notification.to_json())
        except IntegrityError:
            pass  # duplicate row
