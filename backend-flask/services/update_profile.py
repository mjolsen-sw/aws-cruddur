from aws_xray_sdk.core import xray_recorder

from lib.db import db

class UpdateProfile:
  def run(cognito_user_id, bio, display_name):
    with xray_recorder.in_segment('create_activity_run') as segment:
      model = {
        'errors': None,
        'data': None
      }

      if display_name == None or len(display_name) < 1:
        model['errors'] = ['display_name_blank']

      if model['errors']:
        model['data'] = {
          'bio': bio,
          'display_name': display_name
        }
      else:
        handle = UpdateProfile.update_profile(bio, display_name, cognito_user_id)
        data = UpdateProfile.query_users_short(handle)
        model['data'] = data
      segment.put_annotation('data', model['data'])
      return model
   
  def update_profile(bio, display_name, cognito_user_id):
    if bio == None:    
      bio = ''

    sql = db.template('users', 'update')
    params = {
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    }
    handle = db.query_commit(sql, params)

  def query_users_short(handle):
    sql = db.template('users', 'short')
    params = { 'handle': handle }
    data = db.query_object_json(sql, params)
    return data