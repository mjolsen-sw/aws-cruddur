from flask import Blueprint, request
from flask_cors import cross_origin

from lib.utils import model_json
from lib.cognito_jwt_token import auth_checked

from services.home_activities import HomeActivities
from services.notifications_activities import NotificationsActivities
from services.user_activities import UserActivities
from services.create_activity import CreateActivity
from services.create_reply import CreateReply
from services.search_activities import SearchActivities
from services.show_activity import ShowActivity

acts = Blueprint('acts', __name__)

@acts.route("/home", methods=['GET'])
@auth_checked
def data_home():
  data = HomeActivities.run(request.cognito_user_id)
  return data, 200

@acts.route("/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@acts.route("/@<string:handle>", methods=['GET'])
@auth_checked
def data_handle(handle):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = UserActivities.run(handle)
  return model_json(model)

@acts.route("/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  return model_json(model)

@acts.route("", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, request.cognito_user_id, ttl)
  return model_json(model)

@acts.route("/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@acts.route("/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities_reply(activity_uuid):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  model = CreateReply.run(message, request.cognito_user_id, activity_uuid)
  return model_json(model)