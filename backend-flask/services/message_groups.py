from aws_xray_sdk.core import xray_recorder

from lib.db import db
from lib.ddb import ddb

class MessageGroups:
  def run(cognito_user_id):
    with xray_recorder.in_segment('message_groups') as segment:
      model = {
        'errors': [],
        'data': None
      }

      sql = db.template('users','uuid_from_cognito_user_id')
      my_user_uuid = db.query_value(sql, {'cognito_user_id': cognito_user_id})

      print(f"UUID: {my_user_uuid}")

      results = ddb.list_message_groups(my_user_uuid)
      print("list_message_groups:", results)
      segment.put_annotation("cognito_user_id", cognito_user_id)
      segment.put_annotation("user_uuid", my_user_uuid)
      segment.put_annotation("app.results", len(results))

      model['data'] = results
      return model