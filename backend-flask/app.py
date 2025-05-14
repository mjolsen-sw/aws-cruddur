from flask import Flask, jsonify, request
from flask_cors import cross_origin
import os

from lib.cognito_jwt_token import auth_checked
from lib.cors import configure_cors
from lib.rollbar import configure_rollbar

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

# # aws x-ray
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# # aws cloudwatch
# import watchtower
# import logging
# from time import strftime

app = Flask(__name__)

configure_cors(app)
configure_rollbar(app)

# # x-ray
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# XRayMiddleware(app, xray_recorder)

# # Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)

# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response

def model_json(model):
  if len(model['errors']) > 0:
    return jsonify(model['errors']), 422
  else:
    return jsonify(model['data']), 200

@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200

@app.route("/api/message_groups", methods=['GET'])
@auth_checked
def data_message_groups():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = MessageGroups.run(cognito_user_id=request.cognito_user_id)
  return model_json(model)

@app.route("/api/messages/<string:message_group_id>", methods=['GET'])
@auth_checked
def data_messages(message_group_id):
  model = Messages.run(
    cognito_user_id=request.cognito_user_id,
    message_group_id=message_group_id
  )
  return model_json(model)

@app.route("/api/messages", methods=['POST','OPTIONS'])
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

@app.route("/api/profile/update", methods=['POST','OPTIONS'])
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

@app.route("/api/users/@<string:handle>/short")
def data_short(handle):
  data = UsersShort.run(handle)
  return data, 200

@app.route("/api/activities/home", methods=['GET'])
@auth_checked
def data_home():
  data = HomeActivities.run(request.cognito_user_id)
  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
@auth_checked
def data_handle(handle):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = UserActivities.run(handle)
  return model_json(model)

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  return model_json(model)

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, request.cognito_user_id, ttl)
  return model_json(model)

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities_reply(activity_uuid):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  model = CreateReply.run(message, request.cognito_user_id, activity_uuid)
  return model_json(model)

if __name__ == "__main__":
  app.run(debug=True)