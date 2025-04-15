from aws_xray_sdk.core import xray_recorder
from datetime import datetime, timedelta, timezone

from lib.db import db

class HomeActivities:
  def run(username=None):
    with xray_recorder.in_segment('home_activities') as segment:
      now = datetime.now(timezone.utc).astimezone()
      segment.put_annotation("app.now", now.isoformat())
      sql = db.template("activities", "home")
      results = db.query_array_json(sql)
      segment.put_annotation("app.result_length", len(results))
      return results