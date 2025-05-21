from flask import Blueprint, request
from flask_cors import cross_origin
import os

from lib.utils import model_json
from lib.cognito_jwt_token import auth_checked

from services.users_short import UsersShort
from services.update_profile import UpdateProfile

api = Blueprint('api', __name__)

@api.route('/health-check')
def health_check():
  return {'success': True}, 200

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