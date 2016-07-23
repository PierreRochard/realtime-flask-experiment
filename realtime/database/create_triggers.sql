CREATE OR REPLACE FUNCTION table_update_notify() RETURNS trigger AS $$
DECLARE
  id bigint;
BEGIN
  IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
    id = NEW.id;
    PERFORM pg_notify('table_update', json_build_object('table', TG_TABLE_NAME, 'id', id, 'type', TG_OP, 'row', row_to_json(NEW))::text);
  ELSE
    id = OLD.id;
    PERFORM pg_notify('table_update', json_build_object('table', TG_TABLE_NAME, 'id', id, 'type', TG_OP, 'row', row_to_json(OLD))::text);
  END IF;
--   If you wanted to get really fancy, you could create a DIFF from the OLD row to NEW row on updates, and create a change feed

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER users_notify_update ON flask.updates;
CREATE TRIGGER users_notify_update AFTER UPDATE ON flask.updates FOR EACH ROW EXECUTE PROCEDURE table_update_notify();

DROP TRIGGER users_notify_insert ON flask.updates;
CREATE TRIGGER users_notify_insert AFTER INSERT ON flask.updates FOR EACH ROW EXECUTE PROCEDURE table_update_notify();

DROP TRIGGER users_notify_delete ON flask.updates;
CREATE TRIGGER users_notify_delete AFTER DELETE ON flask.updates FOR EACH ROW EXECUTE PROCEDURE table_update_notify();