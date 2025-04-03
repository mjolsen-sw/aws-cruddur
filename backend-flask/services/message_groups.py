import uuid
from datetime import datetime, timedelta, timezone

from lib.db import db
from lib.ddb import ddb

class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': [],
      'data': None
    }

    sql = db.template('users','uuid_from_cognito_user_id')
    my_user_uuid = db.query_value(sql, { 'cognito_user_id': cognito_user_id })

    print(f"UUID: {my_user_uuid}")

    data = ddb.list_message_groups(my_user_uuid)
    print("list_message_groups:", data)

    model['data'] = data
    return model