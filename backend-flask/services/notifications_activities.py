from datetime import datetime, timedelta, timezone
class NotificationsActivities:
  def run():
    now = datetime.now(timezone.utc).astimezone()
    results = [{
      'uuid': 'd05f3dac-4fb2-4497-9588-716e38736002',
      'handle':  'coco',
      'message': 'I am a white unicorn!',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 101,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
        'uuid': '47f19fd6-dd49-49a4-bd9e-e4b12ecb4ddc',
        'reply_to_activity_uuid': 'd05f3dac-4fb2-4497-9588-716e38736002',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'likes_count': 0,
        'replies_count': 0,
        'reposts_count': 0,
        'created_at': (now - timedelta(days=2)).isoformat()
      }],
    }
    ]
    return results