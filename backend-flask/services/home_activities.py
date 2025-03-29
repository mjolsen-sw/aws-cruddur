from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import db

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(username=None):
    with tracer.start_as_current_span("home-activities-seeded-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
      sql = db.template("activities", "home")
      results = db.query_array_json(sql)
      span.set_attribute("app.result_length", len(results))
      return results