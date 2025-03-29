from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import pool, query_wrap_array

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(username=None):
    with tracer.start_as_current_span("home-activities-seeded-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
      
      sql = query_wrap_array("""
        SELECT
          activities.uuid,
          users.display_name,
          users.handle,
          activities.message,
          activities.replies_count,
          activities.reposts_count,
          activities.likes_count,
          activities.reply_to_activity_uuid,
          activities.expires_at,
          activities.created_at
        FROM public.activities
        LEFT JOIN public.users ON users.uuid = activities.user_uuid
        ORDER BY activities.created_at DESC
        """)
      print(sql)
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()
      data = json[0][0]
      print(data)
      span.set_attribute("app.result_length", len(data))
      return data