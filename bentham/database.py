from sqlalchemy import (event, func, UniqueConstraint, Table, Column, Integer, String, MetaData,
                        DateTime, Boolean)
from sqlalchemy.dialects.postgresql import JSONB


metadata = MetaData()

events = Table('events', metadata,
               Column('id', Integer, primary_key=True),
               Column('created_at', DateTime(timezone=True), default=func.now()),
               Column('occurred_at', DateTime(timezone=True)),
               Column('tracker', String),
               Column('source', String),
               Column('message', String),
               Column('raw', String),
               Column('raw_json', JSONB, default={}),
               Column('acknowledged', Boolean, default=False),
               UniqueConstraint('occurred_at', 'tracker', 'source', 'message',
                                name='unique_idx'))

checkins = Table('checkins', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('tracker', String),
                 Column('source', String),
                 Column('checkin', DateTime(timezone=True), default=func.now()),
                 UniqueConstraint('tracker', 'source', name='tracker_source_idx'))


def after_create_events(target, connection, **kwargs):
    connection.execute("""
CREATE OR REPLACE FUNCTION bentham_event_notify() RETURNS trigger AS $$
DECLARE
BEGIN
  PERFORM pg_notify('bentham_events', to_json(NEW)::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS bentham_new_event ON events;

CREATE TRIGGER bentham_new_event
AFTER INSERT ON events
FOR EACH ROW
EXECUTE PROCEDURE bentham_event_notify();""")

event.listen(events, 'after_create', after_create_events)
