DROP TRIGGER IF EXISTS todos_notify_update ON flask.todo_items;
CREATE TRIGGER todos_notify_update
AFTER UPDATE ON flask.todo_items
FOR EACH ROW EXECUTE PROCEDURE table_notify();

DROP TRIGGER IF EXISTS todos_notify_insert ON flask.todo_items;
CREATE TRIGGER todos_notify_insert
AFTER INSERT ON flask.todo_items
FOR EACH ROW EXECUTE PROCEDURE table_notify();

DROP TRIGGER IF EXISTS todos_notify_delete ON flask.todo_items;
CREATE TRIGGER todos_notify_delete
AFTER DELETE ON flask.todo_items
FOR EACH ROW EXECUTE PROCEDURE table_notify();
