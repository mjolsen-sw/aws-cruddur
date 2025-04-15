from aws_xray_sdk.core import xray_recorder

from lib.db import db

class UsersShort:
  def run(handle):
    with xray_recorder.in_segment('users_short') as segment:
      sql = db.template('users','short')
      results = db.query_object_json(sql, {
        'handle': handle
      })
      segment.put_annotation('handle', handle)
      segment.put_annotation('results', results)
      return results