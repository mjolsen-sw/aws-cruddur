import uuid
from aws_xray_sdk.core import xray_recorder
from datetime import datetime, timedelta, timezone

from lib.db import db

class CreateReply:
  def run(message, cognito_user_id, activity_uuid):
    with xray_recorder.in_segment('create_reply_run') as segment:
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
        uuid = CreateReply.create_reply(cognito_user_id, message, activity_uuid)
        data = CreateReply.get_reply_info(uuid)
        CreateReply.update_reply_count(data['reply_to_activity_uuid'])
        model['data'] = data
      return model

  @staticmethod
  def create_reply(cognito_user_id, message, activity_uuid):
    with xray_recorder.in_segment('create_reply_create') as segment:
      sql = db.template("activities", "reply")
      params = { 
        "cognito_user_id": cognito_user_id,
        "message": message,
        "activity_uuid": activity_uuid
        }
      uuid = db.query_commit(sql, params)
      segment.put_annotation("reply.created.uuid", uuid)
      return uuid
    
  @staticmethod
  def get_reply_info(uuid):
    with xray_recorder.in_segment('create_reply_get') as segment:
      sql = db.template("activities", "object")
      params = { "uuid": uuid }
      data = db.query_object_json(sql, params)
      segment.put_annotation("reply.created.data", data)
      return data
  
  @staticmethod
  def update_reply_count(activity_uuid):
    with xray_recorder.in_segment('create_reply_update_count') as segment:
      sql = db.template("activities", "update_reply_count")
      params = { 
        "activity_uuid": activity_uuid
        }
      db.query_commit(sql, params)
      segment.put_annotation("reply.updated.count.uuid", activity_uuid)