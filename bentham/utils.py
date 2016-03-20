from bentham.database import checkins
from sqlalchemy import func
from sqlalchemy.sql import select


def bentham_checkin(tracker, source, db, cfg):
    # @todo use a proper new postgres upsert
    exists = db.execute(select([checkins])
                        .where(checkins.c.tracker == tracker)
                        .where(checkins.c.source == source)).fetchone()

    if exists:
        db.execute(checkins.update()
                   .where(checkins.c.id == exists[0])
                   .values(checkin=func.now()))
    else:
        db.execute(checkins.insert(),
                   tracker=tracker,
                   source=source)
