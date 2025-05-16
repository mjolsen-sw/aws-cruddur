from lib.db import db

class UpdateReplyToActivityUuidMigration:

  def migrate_sql():
    data = """
    UPDATE public.activities
    SET reply_to_activity_uuid = NULL;

    ALTER TABLE public.activities
    ALTER COLUMN reply_to_activity_uuid TYPE UUID USING NULL::uuid;
    """
    return data

  def rollback_sql():
    data = """
    UPDATE public.activities
    SET reply_to_activity_uuid = NULL;

    ALTER TABLE public.activities
    ALTER COLUMN reply_to_activity_uuid TYPE integer USING NULL::integer;
    """
    return data

  def migrate():
    db.query_commit(UpdateReplyToActivityUuidMigration.migrate_sql(), {
    })

  def rollback():
    db.query_commit(UpdateReplyToActivityUuidMigration.rollback_sql(), {
    })

migration = UpdateReplyToActivityUuidMigration