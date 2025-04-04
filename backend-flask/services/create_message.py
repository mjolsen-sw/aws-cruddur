import uuid

from opentelemetry import trace

from lib.db import db
from lib.ddb import ddb

tracer = trace.get_tracer('create.message')

class CreateMessage:
  def run(mode, cognito_user_id, message_group_uuid, message, user_receiver_handle):
    with tracer.start_as_current_span('create-messages-run') as span:
      model = {
        'errors': [],
        'data': None
      }

      if mode == 'update' and (message_group_uuid == None or len(message_group_uuid) < 1):
        model['errors'].append('message_group_uuid_blank')
      elif mode == 'create' and (user_receiver_handle == None or len(user_receiver_handle) < 1):
        model['errors'].append('user_reciever_handle_blank')
      
      if cognito_user_id == None or len(cognito_user_id) < 1:
        model['errors'].append('cognito_user_id_blank')

      if message == None or len(message) < 1:
        model['errors'].append('message_blank')
      elif len(message) > 1024:
        model['errors'].append('message_exceed_max_chars')

      if len(model['errors']) > 0:
        # return what we provided
        model['data'] = {
          'cognito_user_id': cognito_user_id,
          'handle':  user_receiver_handle,
          'message': message
        }
      else:
        sql = db.template('users','create_message_users')
        params = {
          'cognito_user_id': cognito_user_id,
          'user_receiver_handle': user_receiver_handle or ''
        }
        users = db.query_array_json(sql, params)

        my_user    = next((item for item in users if item['kind'] == 'sender'), None)
        other_user = next((item for item in users if item['kind'] == 'recv')  , None)

        print('USERS=[my-user]==')
        print(my_user)
        print('USERS=[other-user]==')
        print(other_user)

        if mode == 'create':
          data = ddb.create_message_group(
            message=message,
            my_user_uuid=my_user['uuid'],
            my_user_display_name=my_user['display_name'],
            my_user_handle=my_user['handle'],
            other_user_uuid=other_user['uuid'],
            other_user_display_name=other_user['display_name'],
            other_user_handle=other_user['handle']
          )
        elif mode == 'update':
          data = ddb.create_message(
            message_group_uuid=message_group_uuid,
            message=message,
            my_user_uuid=my_user['uuid'],
            my_user_display_name=my_user['display_name'],
            my_user_handle=my_user['handle']
          )

        model['data'] = data
        span.set_attribute("message.create.data", data)

      return model