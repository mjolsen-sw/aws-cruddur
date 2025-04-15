from aws_xray_sdk.core import xray_recorder

from lib.db import db
from lib.ddb import ddb

class Messages:
  def run(cognito_user_id, message_group_id):
    with xray_recorder.in_segment('messages') as segment:
      model = {
        'errors': [],
        'data': None
      }

      # sql = db.template('users','uuid_from_cognito_user_id')
      # my_user_uuid = db.query_value(sql, {'cognito_user_id': cognito_user_id})
      # TODO: validate cognito_user_id or my_user_uuid is valid for these messages

      results = ddb.list_messages(message_group_id)

      # segment.put_annotation("cognito_user_id", cognito_user_id)
      # segment.put_annotation("my_user_uuid", my_user_uuid)
      segment.put_annotation("message_group_id", message_group_id)
      segment.put_annotation("app.results", len(results))

      model['data'] = results
      return model