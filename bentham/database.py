from sqlalchemy import (func, UniqueConstraint, Table, Column, Integer, String, MetaData,
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
