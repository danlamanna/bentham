CREATE OR REPLACE FUNCTION bentham_event_notify() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('bentham_events', to_json(NEW)::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS bentham_new_event ON events;

CREATE TRIGGER bentham_new_event
AFTER INSERT ON events
FOR EACH ROW
EXECUTE PROCEDURE bentham_event_notify();
