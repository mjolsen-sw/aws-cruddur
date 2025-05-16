from flask import Blueprint, request
from flask_cors import cross_origin

from lib.utils import model_json
from lib.cognito_jwt_token import auth_checked

from services.message_groups import MessageGroups
from services.messages import Messages
from services.create_message import CreateMessage


msgs = Blueprint('msgs', __name__)

@msgs.route("/groups", methods=['GET'])
@auth_checked
def data_message_groups():
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = MessageGroups.run(cognito_user_id=request.cognito_user_id)
  return model_json(model)

@msgs.route("/<string:message_group_id>", methods=['GET'])
@auth_checked
def data_messages(message_group_id):
  model = Messages.run(
    cognito_user_id=request.cognito_user_id,
    message_group_id=message_group_id
  )
  return model_json(model)

@msgs.route("", methods=['POST','OPTIONS'])
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