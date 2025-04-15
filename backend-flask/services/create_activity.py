from aws_xray_sdk.core import xray_recorder
from datetime import datetime, timedelta, timezone

from lib.db import db

class CreateActivity:
  @staticmethod
  def run(message, cognito_user_id, ttl):
    with xray_recorder.in_segment('create_activity_run') as segment:
      model = {
        'errors': [],
        'data': None
      }

      now = datetime.now(timezone.utc).astimezone()
      segment.put_annotation("app.now", now.isoformat())

      if (ttl == '30-days'):
        ttl_offset = timedelta(days=30) 
      elif (ttl == '7-days'):
        ttl_offset = timedelta(days=7) 
      elif (ttl == '3-days'):
        ttl_offset = timedelta(days=3) 
      elif (ttl == '1-day'):
        ttl_offset = timedelta(days=1) 
      elif (ttl == '12-hours'):
        ttl_offset = timedelta(hours=12) 
      elif (ttl == '3-hours'):
        ttl_offset = timedelta(hours=3) 
      elif (ttl == '1-hour'):
        ttl_offset = timedelta(hours=1) 
      else:
        model['errors'] += ['ttl_blank']

      if message == None or len(message) < 1:
        model['errors'] += ['message_blank'] 
      elif len(message) > 280:
        model['errors'] += ['message_exceed_max_chars']

      if len(model['errors']) > 0:
        model['data'] = {
          'message': message
        }   
      else:
        expires_at = (now + ttl_offset).isoformat()
        uuid = CreateActivity.create_activity(cognito_user_id, message, expires_at)
        data = CreateActivity.get_activity_info(uuid)
        model['data'] = data
      return model

  @staticmethod
  def create_activity(cognito_user_id, message, expires_at):
    with xray_recorder.in_segment('create_activity_create') as segment:
      sql = db.template("activities", "create")
      params = { 
        "cognito_user_id": cognito_user_id,
        "message": message,
        "expires_at": expires_at
        }
      uuid = db.query_commit(sql, params)
      segment.put_annotation("activity.created.uuid", uuid)
      return uuid  
  
  @staticmethod
  def get_activity_info(uuid):
    with xray_recorder.in_segment('create_activity_get') as segment:
      sql = db.template("activities", "object")
      params = { "uuid": uuid }
      data = db.query_object_json(sql, params)
      segment.put_annotation("activity.created.data", data)
      return data
