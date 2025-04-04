from opentelemetry import trace

from lib.db import db
from lib.ddb import ddb

tracer = trace.get_tracer("message.groups")

class MessageGroups:
  def run(cognito_user_id):
    with tracer.start_as_current_span("message-groups-run") as span:
      model = {
        'errors': [],
        'data': None
      }

      sql = db.template('users','uuid_from_cognito_user_id')
      my_user_uuid = db.query_value(sql, {'cognito_user_id': cognito_user_id})

      print(f"UUID: {my_user_uuid}")

      results = ddb.list_message_groups(my_user_uuid)
      print("list_message_groups:", results)
      span.set_attribute("cognito_user_id", cognito_user_id)
      span.set_attribute("user_uuid", my_user_uuid)
      span.set_attribute("app.results", len(results))

      model['data'] = results
      return model