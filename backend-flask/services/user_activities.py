from aws_xray_sdk.core import xray_recorder
from datetime import datetime, timedelta, timezone

from lib.db import db

class UserActivities:
  def run(user_handle):
    with xray_recorder.in_segment('user_activities') as segment:
      model = {
        'errors': [],
        'data': []
      }

      now = datetime.now(timezone.utc).astimezone()
      if user_handle == None or len(user_handle) < 1:
        model['errors'].append('blank_user_handle')
      else:
        sql = db.template("users", "show")
        params = { "handle": user_handle }
        results = db.query_object_json(sql, params)
        model['data'] = results
      segment.put_annotation('results_length', len(model['data']))
      return model