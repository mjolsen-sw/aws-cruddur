from flask import Blueprint, request
from flask_cors import cross_origin
import os

from lib.cognito_jwt_token import auth_checked
from lib.utils import model_json

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *
from services.update_profile import *

api = Blueprint('api', __name__)

@api.route('/health-check')
def health_check():
  return {'success': True}, 200

@api.route("/message_groups", methods=['GET'])
@auth_checked
def data_message_groups():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = MessageGroups.run(cognito_user_id=request.cognito_user_id)
  return model_json(model)

@api.route("/messages/<string:message_group_id>", methods=['GET'])
@auth_checked
def data_messages(message_group_id):
  model = Messages.run(
    cognito_user_id=request.cognito_user_id,
    message_group_id=message_group_id
  )
  return model_json(model)

@api.route("/messages", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_create_message():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401

  message = request.json['message']
  user_receiver_handle = request.json.get('handle', None)
  message_group_uuid = request.json.get('message_group_uuid', None)

  mode = 'create' if message_group_uuid == None else 'update'

  model = CreateMessage.run(
    mode=mode,
    cognito_user_id=request.cognito_user_id,
    message_group_uuid=message_group_uuid,
    message=message,
    user_receiver_handle=user_receiver_handle
  )
  return model_json(model)

@api.route("/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_update_profile():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401

  bio          = request.json.get('bio', None)
  display_name = request.json.get('display_name', None)

  model = UpdateProfile.run(
    cognito_user_id=request.cognito_user_id,
    bio=bio,
    display_name=display_name
  )
  return model_json(model)

@api.route("/users/@<string:handle>/short")
def data_short(handle):
  data = UsersShort.run(handle)
  return data, 200

@api.route("/activities/home", methods=['GET'])
@auth_checked
def data_home():
  data = HomeActivities.run(request.cognito_user_id)
  return data, 200

@api.route("/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@api.route("/activities/@<string:handle>", methods=['GET'])
@auth_checked
def data_handle(handle):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = UserActivities.run(handle)
  return model_json(model)

@api.route("/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  return model_json(model)

@api.route("/activities", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, request.cognito_user_id, ttl)
  return model_json(model)

@api.route("/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@api.route("/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities_reply(activity_uuid):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  model = CreateReply.run(message, request.cognito_user_id, activity_uuid)
  return model_json(model)