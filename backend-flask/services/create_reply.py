import uuid
from datetime import datetime, timedelta, timezone

class CreateReply:
  def run(message, cognito_user_id, activity_uuid):
    model = {
      'errors': [],
      'data': None
    }

    if activity_uuid == None or len(activity_uuid) < 1:
      model['errors'].append('activity_uuid_blank')

    if message == None or len(message) < 1:
      model['errors'].append('message_blank')
    elif len(message) > 1024:
      model['errors'].append('message_exceed_max_chars')

    if len(model['errors']) > 0:
      # return what we provided
      model['data'] = {
        'cognito_user_id': cognito_user_id,
        'message': message,
        'reply_to_activity_uuid': activity_uuid
      }
    else:
      now = datetime.now(timezone.utc).astimezone()
      model['data'] = {
        'uuid': uuid.uuid4(),
        'display_name': 'Andrew Brown',
        'handle':  user_handle,
        'message': message,
        'created_at': now.isoformat(),
        'reply_to_activity_uuid': activity_uuid
      }
    return model