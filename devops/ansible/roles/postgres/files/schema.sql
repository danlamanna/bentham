CREATE TABLE IF NOT EXISTS events (
       id SERIAL,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
       occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
       tracker VARCHAR NOT NULL,
       source_identifier VARCHAR NOT NULL,
       event_hash BYTEA NOT NULL,
       message VARCHAR NOT NULL,
       raw_event TEXT,
       raw_event_json JSON,
       ack BOOLEAN DEFAULT FALSE,
       UNIQUE(source_identifier, event_hash)
);
