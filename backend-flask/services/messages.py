from opentelemetry import trace

from lib.db import db
from lib.ddb import ddb

tracer = trace.get_tracer("user.messages")

class Messages:
  def run(cognito_user_id, message_group_id):
    with tracer.start_as_current_span("user-messages-run") as span:
      model = {
        'errors': [],
        'data': None
      }

      # sql = db.template('users','uuid_from_cognito_user_id')
      # my_user_uuid = db.query_value(sql, {'cognito_user_id': cognito_user_id})
      # TODO: validate cognito_user_id or my_user_uuid is valid for these messages

      results = ddb.list_messages(message_group_id)

      # span.set_attribute("cognito_user_id", cognito_user_id)
      # span.set_attribute("my_user_uuid", my_user_uuid)
      span.set_attribute("message_group_id", message_group_id)
      span.set_attribute("app.results", len(results))

      model['data'] = results
      return model