from aws_xray_sdk.core import xray_recorder
from datetime import datetime, timedelta, timezone

class UserActivities:
  def run(user_handle):
    with xray_recorder.in_segment('user_activities') as segment:
      model = {
        'errors': None,
        'data': None
      }

      now = datetime.now(timezone.utc).astimezone()
      if user_handle == None or len(user_handle) < 1:
        model['errors'] = ['blank_user_handle']
      else:
        now = datetime.now()
        results = [{
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Andrew Brown',
          'message': 'Cloud is fun!',
          'created_at': (now - timedelta(days=1)).isoformat(),
          'expires_at': (now + timedelta(days=31)).isoformat()
        }]
        model['data'] = results
      segment.put_annotation('now', now.isoformat())
      segment.put_annotation('results_length', len(model['data']))
      return model